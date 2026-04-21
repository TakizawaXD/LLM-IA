import streamlit as st

def render_resume_tab(df, stats):
    st.header("Informacion General")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Pasajeros", len(df))
    col2.metric("Tasa de Supervivencia", f"{stats['survival_rate']*100:.1f}%")
    col3.metric("Edad Media", f"{stats['avg_age']:.1f}")
    col4.metric("Tarifa Media", f"${stats['avg_fare']:.1f}")
    
    st.subheader("Lista de Pasajeros")
    st.dataframe(df.head(20), use_container_width=True)
