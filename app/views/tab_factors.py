import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

def render_factors_tab(trainer):
    st.header("Evaluación del Modelo y Métricas")
    
    if not trainer or not trainer.metrics:
        st.warning("El modelo no ha sido entrenado. Por favor dale clic a 'Iniciar Presentacion'.")
        return

    st.subheader("1. Rendimiento Predictivo")
    st.write("Comparativa entre los dos algoritmos de IA entrenados en tiempo real.")
    
    rf_m = trainer.metrics["RandomForest"]
    lr_m = trainer.metrics["LogisticRegression"]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        diff = rf_m['accuracy'] - lr_m['accuracy']
        st.metric("Precisión (Random Forest)", f"{rf_m['accuracy']:.1%}", f"{diff:+.1%} vs Reg. Logística")
    with col2:
        st.metric("F1-Score (Random Forest)", f"{rf_m['f1']:.2f}")
    with col3:
        st.metric("Precisión (Reg. Logística)", f"{lr_m['accuracy']:.1%}")
    with col4:
        st.metric("F1-Score (Reg. Logística)", f"{lr_m['f1']:.2f}")
        
    st.markdown("---")
    col_cm, col_fi = st.columns(2)
    
    with col_cm:
        st.subheader("2. Matriz de Confusión")
        st.write("Aciertos vs Errores en la predicción (Random Forest)")
        cm = rf_m['confusion_matrix']
        z = [[cm[1][1], cm[0][1]], [cm[1][0], cm[0][0]]]
        x = ['Predijo Sobrevive', 'Predijo Fallece']
        y = ['Real Realidad: Sobrevive', 'Real Realidad: Fallece']
        
        fig_cm = ff.create_annotated_heatmap(z, x=x, y=y, colorscale='viridis')
        fig_cm.update_layout(height=400, margin=dict(l=0, r=0, b=0, t=30))
        st.plotly_chart(fig_cm, use_container_width=True)

    with col_fi:
        st.subheader("3. Factores Determinantes")
        st.write("Peso de cada variable en la decisión del modelo")
        if trainer.feature_importance:
            fi_df = pd.DataFrame(list(trainer.feature_importance.items()), columns=['Caracteristica', 'Nivel de Importancia'])
            name_map = {
                'Sex_encoded': 'Género', 'Pclass': 'Clase económica', 'Fare': 'Tarifa',
                'Age': 'Edad', 'FamilySize': 'Acompañantes', 'IsAlone': 'Aislamiento',
                'Embarked_encoded': 'Puerto origen', 'SibSp': 'Hermanos', 'Parch': 'Hijos/Padres'
            }
            fi_df['Caracteristica'] = fi_df['Caracteristica'].map(name_map).fillna(fi_df['Caracteristica'])
            
            fig_bar = px.bar(fi_df, x='Nivel de Importancia', y='Caracteristica', orientation='h', 
                             color='Nivel de Importancia', color_continuous_scale='teal')
            fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, height=400, margin=dict(l=0, r=0, b=0, t=30))
            st.plotly_chart(fig_bar, use_container_width=True)
