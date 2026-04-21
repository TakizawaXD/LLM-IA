import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
        /* Estilos Globales */
        .stApp {
            background: linear-gradient(135deg, #0a1128, #1c2541, #0a1128);
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
