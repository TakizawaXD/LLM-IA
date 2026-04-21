import streamlit as st
from simulation import SurvivalSimulator
from utils import fetch_wikipedia_photo, get_et_url

def render_interactive_tab(df, trainer):
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
                    icon = "🟢" if row['Survived'] == 1 else "🔴"
                    with st.expander(f"{icon} {row['Name']} - {estado}"):
                        p_col1, p_col2 = st.columns([1, 3])
                        
                        with p_col1:
                            real_img = fetch_wikipedia_photo(row['Name'])
                            if real_img:
                                st.image(real_img, use_container_width=True, caption=row['Name'])
                            else:
                                bg_color = "2A4B7C" if row['Sex'] == 'male' else "7c2a3e"
                                name_url = str(row['Name']).replace(" ", "+")
                                img_url = f"https://ui-avatars.com/api/?name={name_url}&background={bg_color}&color=fff&size=150"
                                st.image(img_url, use_container_width=True)
                            
                            et_link = get_et_url(row['Name'], row['Survived'])
                            st.markdown(f"[📖 Perfil en Encyclopedia Titanica]({et_link})")
                        
                        with p_col2:
                            st.markdown(f"**Edad:** {row['Age']} años")
                            st.markdown(f"**Género:** {row['Sex'].capitalize()}")
                            st.markdown(f"**Clase Económica:** Clase {row['Pclass']}")
                            st.markdown(f"**Ticket & Cabina:** {row['Ticket']} | {row.get('Cabin', 'Desconocida')}")
                            st.markdown(f"**Tarifa:** ${row['Fare']:.2f}")
                            st.markdown(f"**Compañantes (Hermanos/Padres):** {row['SibSp']} / {row['Parch']}")
                            st.markdown(f"**Puerto:** {row['Embarked']}")

    with b_col2:
        st.subheader("Simulador de Supervivencia")
        st.markdown("Ingresa tus datos principales, las variables tecnicas fueron automatizadas para dar un resultado rapido y preciso.")
        
        with st.form("survival_form"):
            st.markdown("**Por favor completa estos 8 datos clave para tu simulación:**")
            col_f1, col_f2 = st.columns(2)
            
            with col_f1:
                u_age = st.slider("Tu Edad", 0, 100, 25)
                u_sex = st.selectbox("Tu Genero", ["Masculino", "Femenino"])
                u_class = st.selectbox("Clase de Pasajero", [1, 2, 3], help="1=Primera Clase (Lujo), 3=Tercera Clase (Economica)")
                u_fare = st.number_input("Tarifa del Boleto", 0.0, 512.32, 32.2)
                
            with col_f2:
                u_sibsp = st.number_input("Hermanos / Conyuges a Bordo", 0, 10, 0)
                u_parch = st.number_input("Padres / Hijos a Bordo", 0, 10, 0)
                u_embarked = st.selectbox("Puerto de Embarque", ["Southampton", "Cherbourg", "Queenstown"])
                u_alone = st.selectbox("Viajas Solo?", ["Sí", "No"])
            
            submitted = st.form_submit_button("Predecir")
            
            if submitted:
                if trainer and trainer.best_model:
                    simulator = SurvivalSimulator(trainer)
                    res = simulator.simulate(u_age, u_sex, u_class, u_sibsp, u_parch, u_fare, u_embarked, u_alone)
                    
                    try:
                        from database import db_manager
                        db_manager.log_simulation({
                            'age': u_age, 'sex': u_sex, 'pclass': u_class,
                            'sibsp': u_sibsp, 'parch': u_parch, 'fare': u_fare,
                            'embarked': u_embarked, 'alone': u_alone,
                            'prediction_outcome': int(res['prediction']), 
                            'survival_probability': float(res['survive_prob'])
                        })
                    except BaseException:
                        pass
                    
                    st.markdown("---")
                    st.subheader("Tu Estadistica Detallada de Supervivencia")
                    
                    col_res1, col_res2 = st.columns(2)
                    with col_res1:
                        st.metric("Probabilidad de Sobrevivir", f"{res['survive_prob']:.1f}%")
                    with col_res2:
                        st.metric("Probabilidad de Fallecer", f"{res['die_prob']:.1f}%")
                        
                    st.progress(int(res['survive_prob']) if res['survive_prob'] < 100 else 100)
                    
                    if res['prediction'] == 1:
                        st.success(f"Sobreviviste. La balanza historica esta un {res['survive_prob']:.1f}% a tu favor.")
                    else:
                        st.error(f"Falleciste. Tienes un {res['die_prob']:.1f}% de estadistica en tu contra.")
                        
                    st.markdown("#### Desglose de Factores Historicos:")
                    st.markdown("Asi afectaron tus decisiones y perfil a tu puntuacion final:")
                    
                    for p in res['puntos']:
                        st.write(p)
                else:
                    st.warning("El simulador no esta listo. Por favor dale a 'Iniciar Presentacion' primero.")
