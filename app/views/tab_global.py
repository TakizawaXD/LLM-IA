import streamlit as st

def render_global_tab(df, viz):
    st.header("Flujo de Pasajeros")
    st.markdown(
        "Visualiza como se agrupan los pasajeros segun su clase y resultado final. "
        "Pasa el cursor sobre las lineas para ver la cantidad de personas."
    )
    st.plotly_chart(viz.plot_global_parallel_categories(df), use_container_width=True)
