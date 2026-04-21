import streamlit as st

def render_charts_tab(df, viz):
    st.header("Graficos Detallados")
    r1_c1, r1_c2 = st.columns(2)
    r1_c1.plotly_chart(viz.plot_survival_by_sex(df), use_container_width=True)
    r1_c2.plotly_chart(viz.plot_survival_by_class(df), use_container_width=True)
    
    st.plotly_chart(viz.plot_dot_plot(df), use_container_width=True)
    
    r2_c1, r2_c2 = st.columns(2)
    r2_c1.plotly_chart(viz.plot_fare_by_class_boxplot(df), use_container_width=True)
    r2_c2.plotly_chart(viz.plot_line_with_reference(df), use_container_width=True)
