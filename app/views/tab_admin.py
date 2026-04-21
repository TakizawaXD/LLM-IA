import streamlit as st
import pandas as pd
from database import db_manager

def render_admin_tab():
    st.header("Base de Datos (Logs)")
    st.markdown("Historial de simulaciones realizadas por los usuarios en la aplicación.")
    
    try:
        # Check if table exists
        query = "SELECT * FROM simulation_logs ORDER BY timestamp DESC"
        df = db_manager.load_query(query)
        if df.empty:
            st.info("No hay simulaciones registradas en la base de datos todavía. Ve a la pestaña 'Simulador' e inténtalo.")
        else:
            st.metric("Total Simulaciones Realizadas", len(df))
            st.dataframe(df, use_container_width=True)
            
            # Simple summary for the admin
            if len(df) > 0:
                st.subheader("Estadísticas Rápidas de Simulaciones")
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Géneros más simulados:**")
                    st.bar_chart(df['sex'].value_counts())
                with col2:
                    st.write("**Tasa media de supervivencia simulada (%):**")
                    st.line_chart(df['survival_probability'])
    except Exception as e:
        st.error(f"No se pudo cargar la base de datos: {e}")
