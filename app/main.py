import streamlit as st
import pandas as pd
from config import config
from data_loader import DataLoader
from cleaning import DataCleaner
from data_stats import DataStatistics
from visualizations import Visualizer
from model import ModelTrainer

# --- PAGE CONFIG ---
st.set_page_config(page_title="Presentacion del Titanic", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* Estilos Globales */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        font-family: 'Inter', sans-serif;
    }
    
    /* Metricas */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 800;
        color: #00d4ff;
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: transform 0.3s;
    }
    .stMetric:hover { transform: translateY(-5px); }

    /* Pestanas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px 10px 0 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-bottom: none;
        color: white;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(0, 212, 255, 0.2) !important;
        color: #00d4ff !important;
        font-weight: bold;
    }
    
    /* Headers */
    h1, h2, h3 { color: #00d4ff !important; }
    
    /* Text Input & Buttons */
    .stTextInput input, .stSelectbox [data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border-radius: 8px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00d4ff 0%, #007bb5 100%);
        color: white;
        border-radius: 20px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
        transition: transform 0.2s;
    }
    .stButton>button:hover { transform: scale(1.05); color: white; }
</style>
""", unsafe_allow_html=True)

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
    st.image("https://upload.wikimedia.org/wikipedia/commons/f/fd/RMS_Titanic_3.jpg", use_container_width=True)
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
    tab1, tab_global, tab3, tab4, tab5 = st.tabs(["Resumen", "Vista General", "Graficos", "Variables Importantes", "Simulador y Busqueda"])
    
    df = st.session_state.processed_df
    stats = DataStatistics.get_full_stats(df)

    with tab1:
        st.header("Informacion General")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Pasajeros", len(df))
        col2.metric("Tasa de Supervivencia", f"{stats['survival_rate']*100:.1f}%")
        col3.metric("Edad Media", f"{stats['avg_age']:.1f}")
        col4.metric("Tarifa Media", f"${stats['avg_fare']:.1f}")
        
        st.subheader("Lista de Pasajeros")
        st.dataframe(df.head(20), use_container_width=True)

    with tab_global:
        st.header("Flujo de Pasajeros")
        st.markdown(
            "Visualiza como se agrupan los pasajeros segun su clase y resultado final. "
            "Pasa el cursor sobre las lineas para ver la cantidad de personas."
        )
        st.plotly_chart(viz.plot_global_parallel_categories(df), use_container_width=True)

    with tab3:
        st.header("Graficos Detallados")
        r1_c1, r1_c2 = st.columns(2)
        r1_c1.plotly_chart(viz.plot_survival_by_sex(df), use_container_width=True)
        r1_c2.plotly_chart(viz.plot_survival_by_class(df), use_container_width=True)
        
        st.plotly_chart(viz.plot_dot_plot(df), use_container_width=True)
        

        
        r2_c1, r2_c2 = st.columns(2)
        r2_c1.plotly_chart(viz.plot_fare_by_class_boxplot(df), use_container_width=True)
        r2_c2.plotly_chart(viz.plot_line_with_reference(df), use_container_width=True)

    with tab4:
        st.header("Factores Determinantes")
        st.write("Estos fueron los factores que mas influyeron en que un pasajero se salvara o no (basado en estadistica historica).")
        if st.session_state.trainer.feature_importance:
            fi_df = pd.DataFrame(list(st.session_state.trainer.feature_importance.items()), columns=['Caracteristica', 'Nivel de Importancia'])
            # Filtramos para mostrar los nombres mas amigables
            name_map = {
                'Sex_encoded': 'Genero', 'Pclass': 'Clase de Boleto', 'Fare': 'Tarifa Pagada',
                'Age': 'Edad', 'FamilySize': 'Tamano Familia', 'IsAlone': 'Viajaba Solo',
                'Embarked_encoded': 'Puerto Embarque', 'SibSp': 'Hermanos o Pareja', 'Parch': 'Padres o Hijos'
            }
            fi_df['Caracteristica'] = fi_df['Caracteristica'].map(name_map)
            st.bar_chart(fi_df.set_index('Caracteristica'))

    with tab5:
        st.header("Seccion Interactiva")
        
        b_col1, b_col2 = st.columns(2)
        
        with b_col1:
            st.subheader("Buscar Pasajero Real")
            search_query = st.text_input("Ingresa un apellido o nombre:")
            
            if search_query:
                results = df[df['Name'].str.contains(search_query, case=False, na=False)]
                if results.empty:
                    st.warning(f"No se encontro ningun pasajero con el nombre: '{search_query}'")
                else:
                    st.success(f"Se encontraron {len(results)} pasajeros:")
                    for index, row in results.iterrows():
                        estado = "Sobrevivio" if row['Survived'] == 1 else "Fallecio"
                        st.markdown(f"- **{row['Name']}** ({row['Sex']}, Clase {row['Pclass']}) - **{estado}**")

        with b_col2:
            st.subheader("Simulador de Supervivencia")
            st.markdown("Ingresa tus datos principales, las variables tecnicas fueron automatizadas para dar un resultado rapido y preciso.")
            
            with st.form("survival_form"):
                u_age = st.slider("Tu Edad", 0, 100, 25)
                u_sex = st.selectbox("Tu Genero", ["Masculino", "Femenino"])
                u_class = st.selectbox("Clase de Pasajero", [1, 2, 3], help="1=Primera Clase (Lujo), 3=Tercera Clase (Economica)")
                u_companions = st.number_input("Numero de acompanantes familiares", 0, 10, 0)
                
                submitted = st.form_submit_button("Predecir")
                
                if submitted:
                    if st.session_state.get('trainer') and st.session_state.trainer.best_model:
                        # Logica interna para preparar variables ocultas al usuario
                        sex_enc = 1 if u_sex == "Femenino" else 0
                        fam_size = u_companions + 1
                        is_alone = 1 if fam_size == 1 else 0
                        
                        # Aproximacion de tarifa por clase y default embarkation para simplificar
                        fare_aprox = {1: 80, 2: 20, 3: 10}[u_class]
                        emb_enc = 0 # Default Southampton
                        sibsp = u_companions // 2 # Aproximacion
                        parch = u_companions - sibsp
                        
                        input_df = pd.DataFrame([{
                            'Pclass': u_class,
                            'Age': u_age,
                            'SibSp': sibsp,
                            'Parch': parch,
                            'Fare': fare_aprox,
                            'FamilySize': fam_size,
                            'IsAlone': is_alone,
                            'Sex_encoded': sex_enc,
                            'Embarked_encoded': emb_enc
                        }])
                        
                        prediction = st.session_state.trainer.predict(input_df)[0]
                        
                        # Extraemos probabilidad
                        proba = st.session_state.trainer.best_model.predict_proba(input_df)[0]
                        survive_prob = proba[1] * 100
                        die_prob = proba[0] * 100
                        
                        st.markdown("---")
                        st.subheader("Tu Estadistica Detallada de Supervivencia")
                        
                        col_res1, col_res2 = st.columns(2)
                        with col_res1:
                            st.metric("Probabilidad de Sobrevivir", f"{survive_prob:.1f}%")
                        with col_res2:
                            st.metric("Probabilidad de Fallecer", f"{die_prob:.1f}%")
                            
                        st.progress(int(survive_prob) if survive_prob < 100 else 100)
                        
                        if prediction == 1:
                            st.success(f"Sobreviviste. La balanza historica esta un {survive_prob:.1f}% a tu favor.")
                        else:
                            st.error(f"Falleciste. Tienes un {die_prob:.1f}% de estadistica en tu contra.")
                            
                        st.markdown("#### Desglose de Factores Historicos:")
                        st.markdown("Asi afectaron tus decisiones y perfil a tu puntuacion final:")
                        
                        puntos = []
                        if u_sex == "Femenino":
                            puntos.append("- **Punto a favor (Genero):** Las mujeres tuvieron gran prioridad en los botes salvavidas (Regla de oro: 'Mujeres y ninos primero').")
                        else:
                            puntos.append("- **Punto en contra (Genero):** Los hombres tuvieron la menor prioridad de rescate por parte de la tripulacion.")
                            
                        if u_class == 1:
                            puntos.append("- **Punto a favor (Clase):** Estar en Primera Clase te situo en las cubiertas superiores, mas cerca de los botes.")
                        elif u_class == 2:
                            puntos.append("- **Punto neutral (Clase):** Estar en Segunda Clase te dio posibilidades intermedias, ni muy lejos ni tan cerca.")
                        else:
                            puntos.append("- **Punto en contra (Clase):** Estar en Tercera Clase (economica) te ubico en la parte mas baja del barco, complicando muchisimo el escape.")
                            
                        if u_age < 12:
                            puntos.append("- **Punto a favor (Edad):** Como niño, se te dio absoluta prioridad de rescate en el caos.")
                        elif u_age > 60:
                            puntos.append("- **Punto en contra (Edad):** Tristemente, la agilidad requerida para navegar multitudes y escaleras jugo en tu contra.")
                            
                        if u_companions in [1, 2, 3]:
                            puntos.append("- **Punto a favor (Acompanantes):** Viajar con un pequeno grupo aumento tus chances, ya que se ayudaron mutuamente a encontrar rutas.")
                        elif u_companions >= 4:
                            puntos.append("- **Punto en contra (Acompanantes):** Viajar con grupos tan grandes impidió coordinarse o hallar botes vacios para todos.")
                        else:
                            puntos.append("- **Punto en contra (Acompanantes):** Al ir completamente solo, careciste de una red de ayuda (desapareces más fácil en el caos).")
                            
                        for p in puntos:
                            st.write(p)
                    else:
                        st.warning("El simulador no esta listo. Por favor dale a 'Iniciar Presentacion' primero.")
