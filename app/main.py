import streamlit as st
import pandas as pd
from config import config
from data_loader import DataLoader
from cleaning import DataCleaner
from data_stats import DataStatistics
from visualizations import Visualizer
from model import ModelTrainer

from style import inject_custom_css
from views import (
    render_resume_tab,
    render_global_tab,
    render_charts_tab,
    render_factors_tab,
    render_interactive_tab,
    render_admin_tab
)

# --- PAGE CONFIG ---
st.set_page_config(page_title="Presentacion del Titanic", layout="wide")

# --- CUSTOM CSS ---
inject_custom_css()

# --- SESSION STATE ---
if 'processed_df' not in st.session_state:
    st.session_state.processed_df = None
if 'model_metrics' not in st.session_state:
    st.session_state.model_metrics = None

# --- COMPONENTS ---
loader = DataLoader()
cleaner = DataCleaner()
viz = Visualizer()
trainer = ModelTrainer()

# --- SIDEBAR ---
with st.sidebar:
    st.title("Presentacion Titanic")
    st.markdown("---")
    
    if st.button("Iniciar Presentacion", type="primary"):
        with st.spinner("Cargando informacion..."):
            from database import db_manager
            raw_df = loader.load_data()
            processed_df = cleaner.process(raw_df)
            st.session_state.processed_df = processed_df
            db_manager.save_dataframe(processed_df, "passengers_cleaned")
            
            metrics = trainer.train(processed_df)
            st.session_state.model_metrics = metrics
            st.session_state.trainer = trainer
            st.success("Informacion lista")

    st.markdown("---")
    if st.session_state.processed_df is not None:
        csv = st.session_state.processed_df.to_csv(index=False).encode('utf-8')
        st.download_button("Descargar Resultados", data=csv, file_name="resultados.csv", mime="text/csv")

# --- MAIN CONTENT ---
st.title("Analisis Historico del Titanic")

if st.session_state.processed_df is None:
    st.warning("Por favor, haz clic en 'Iniciar Presentacion' en el panel lateral para comenzar.")
else:
    tab1, tab_global, tab3, tab4, tab5, tab6 = st.tabs(["Resumen", "Vista General", "Graficos", "Evaluación del Modelo", "Simulador y Busqueda", "Logs DB"])
    
    df = st.session_state.processed_df
    stats = DataStatistics.get_full_stats(df)

    with tab1:
        render_resume_tab(df, stats)

    with tab_global:
        render_global_tab(df, viz)

    with tab3:
        render_charts_tab(df, viz)

    with tab4:
        render_factors_tab(st.session_state.trainer)

    with tab5:
        render_interactive_tab(df, st.session_state.trainer)

    with tab6:
        render_admin_tab()
