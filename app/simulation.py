import pandas as pd
from typing import Tuple, List, Dict

class SurvivalSimulator:
    def __init__(self, trainer):
        self.trainer = trainer

    def simulate(self, u_age: int, u_sex: str, u_class: int, u_sibsp: int, u_parch: int, u_fare: float, u_embarked: str, u_alone: str) -> Dict:
        """
        Calculates survival probability and historical points based on user inputs.
        """
        # Feature Engineering for Model
        sex_enc = 1 if u_sex == "Femenino" else 0
        emb_enc = {'Southampton': 0, 'Cherbourg': 1, 'Queenstown': 2}.get(u_embarked, 0)
        is_alone = 1 if u_alone == "Sí" else 0
        
        if is_alone == 1:
            u_sibsp = 0
            u_parch = 0
            fam_size = 1
        else:
            fam_size = u_sibsp + u_parch + 1
            if fam_size == 1:
                is_alone = 1 # Force it if they forgot
        
        input_df = pd.DataFrame([{
            'Pclass': u_class,
            'Age': u_age,
            'SibSp': u_sibsp,
            'Parch': u_parch,
            'Fare': u_fare,
            'FamilySize': fam_size,
            'IsAlone': is_alone,
            'Sex_encoded': sex_enc,
            'Embarked_encoded': emb_enc
        }])
        
        prediction = self.trainer.predict(input_df)[0]
        
        # Probabilities
        proba = self.trainer.best_model.predict_proba(input_df)[0]
        survive_prob = proba[1] * 100
        die_prob = proba[0] * 100
        
        # Historical rules
        puntos = []
        
        # 1. Genero
        if u_sex == "Femenino":
            puntos.append("- **Punto a favor (Género):** Las mujeres tuvieron gran prioridad en los botes salvavidas (Regla de oro: 'Mujeres y niños primero').")
        else:
            puntos.append("- **Punto en contra (Género):** Los hombres tuvieron la menor prioridad de rescate por parte de la tripulación.")
            
        # 2. Clase
        if u_class == 1:
            puntos.append("- **Punto a favor (Clase):** Estar en Primera Clase te situó en las cubiertas superiores, más cerca de los botes.")
        elif u_class == 2:
            puntos.append("- **Punto neutral (Clase):** Estar en Segunda Clase te dio posibilidades intermedias.")
        else:
            puntos.append("- **Punto en contra (Clase):** Estar en Tercera Clase te ubicó en la parte más baja del barco, complicando el escape.")
            
        # 3. Edad
        if u_age < 12:
            puntos.append("- **Punto a favor (Edad):** Como niño, se te dio absoluta prioridad de rescate en el caos.")
        elif u_age > 60:
            puntos.append("- **Punto en contra (Edad):** Tristemente, la agilidad requerida para navegar multitudes y escaleras jugó en tu contra.")
        else:
            puntos.append("- **Punto neutral (Edad):** Tu edad de adulto te dio resistencia física, pero no prioridad en los botes.")
            
        # 4. Embarque
        if u_embarked == "Cherbourg":
            puntos.append("- **Punto a favor (Puerto):** Históricamente, los embarcados en Cherbourg tuvieron mayor porcentaje de supervivencia (muchos eran de 1ra clase).")
        elif u_embarked == "Southampton":
            puntos.append("- **Punto neutral (Puerto):** Southampton fue el puerto principal, con mayoría de tripulación y 3ra clase.")
        else:
            puntos.append("- **Punto en contra (Puerto):** Queenstown albergó casi exclusivamente emigrantes de 3ra clase.")

        # 5. Tarifa
        if u_fare > 50:
            puntos.append("- **Punto a favor (Tarifa):** Un boleto costoso a menudo garantizaba mejor ubicación e información temprana sobre el hundimiento.")
        elif u_fare < 15:
            puntos.append("- **Punto en contra (Tarifa):** Las tarifas más bajas se tradujeron en camarotes compartidos profundo en el casco del barco.")

        # 6. Compañantes (SibSp / Parch)
        if u_sibsp > 2 or u_parch > 2:
            puntos.append("- **Punto en contra (Red Familiar):** Buscar a varios familiares ralentizó dramáticamente las posibilidades de escapar juntos.")
        elif u_sibsp in [1, 2] or u_parch in [1, 2]:
            puntos.append("- **Punto a favor (Red Familiar):** Estar con pareja o padres facilitó organizarse y pedir ayuda mutua.")

        # 7. Soledad absoluta
        if is_alone == 1:
            puntos.append("- **Punto crítico (Soledad):** Ir completamente solo significa que nadie te busca si te quedas atrapado, aunque facilita colarse en un bote vacío.")

        # 8. Combinaciones fatales / salvadoras
        if u_class == 3 and u_sex == "Masculino" and u_age > 18:
            puntos.append("- **Predicción Fatal (Perfil):** Hombre adulto en tercera clase es estadísticamente el perfil con menor tasa de supervivencia.")
        elif u_class == 1 and u_sex == "Femenino":
            puntos.append("- **Predicción Segura (Perfil):** Mujer en primera clase es el perfil con garantías de rescate casi totales (97% se salvaron).")

        return {
            "prediction": prediction,
            "survive_prob": survive_prob,
            "die_prob": die_prob,
            "puntos": puntos
        }
