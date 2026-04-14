import pandas as pd
import numpy as np
from typing import Tuple
from tracking import tracker
from utils import app_logger

class DataCleaner:
    """Handles all data cleaning and feature engineering steps."""

    @staticmethod
    def process(df: pd.DataFrame) -> pd.DataFrame:
        """Executes the full cleaning pipeline."""
        df_clean = df.copy()
        
        # 1. Eliminar duplicados
        before = df_clean.copy()
        df_clean.drop_duplicates(inplace=True)
        tracker.log("Limpiar Duplicados", [], before, df_clean, "Se eliminaron las filas idénticas.")
        
        # 2. Imputar Edades faltantes
        before = df_clean.copy()
        median_age = df_clean['Age'].median()
        df_clean['Age'] = df_clean['Age'].fillna(median_age)
        tracker.log("Imputar Edad", ["Age"], before, df_clean, f"Se rellenaron las edades faltantes con la mediana ({median_age}).")
        
        # 3. Imputar Embarque (Embarked)
        before = df_clean.copy()
        mode_embarked = df_clean['Embarked'].mode()[0]
        df_clean['Embarked'] = df_clean['Embarked'].fillna(mode_embarked)
        tracker.log("Imputar Embarque", ["Embarked"], before, df_clean, f"Se rellenó el puerto de embarque con la moda ({mode_embarked}).")
        
        # 4. Manejar Cabina (Cabin)
        before = df_clean.copy()
        df_clean['Cabin'] = df_clean['Cabin'].fillna("Unknown")
        tracker.log("Manejar Cabina", ["Cabin"], before, df_clean, "Se reemplazaron los valores nulos de Cabina por 'Unknown'.")
        
        # 5. Feature Engineering: Tamaño Familia
        before = df_clean.copy()
        df_clean['FamilySize'] = df_clean['SibSp'] + df_clean['Parch'] + 1
        tracker.log("Variable: TamañoFamilia", ["FamilySize"], before, df_clean, "Creado TamañoFamilia = SibSp + Parch + 1.")
        
        # 6. Feature Engineering: ¿Está Solo? (IsAlone)
        before = df_clean.copy()
        df_clean['IsAlone'] = (df_clean['FamilySize'] == 1).astype(int)
        tracker.log("Variable: IsAlone", ["IsAlone"], before, df_clean, "Creada columna binaria IsAlone.")
        
        # 7. Categorías de Tarifa
        before = df_clean.copy()
        df_clean['FareCategory'] = pd.qcut(df_clean['Fare'], 4, labels=['Baja', 'Media', 'Alta', 'Muy Alta'])
        tracker.log("Variable: CategoriaTarifa", ["FareCategory"], before, df_clean, "Tarifa agrupada en 4 cuartiles.")
        
        # 8. Grupos de Edad
        before = df_clean.copy()
        bins = [0, 12, 18, 35, 60, 100]
        labels = ['Niño', 'Adolescente', 'Joven Adulto', 'Adulto', 'Senior']
        df_clean['AgeGroup'] = pd.cut(df_clean['Age'], bins=bins, labels=labels)
        tracker.log("Variable: GrupoEdad", ["AgeGroup"], before, df_clean, "Edad agrupada por etapas de vida.")
        
        # 9. Encoding (Convert to Numeric for Model)
        # We keep original columns for viz but add encoded versions
        df_clean['Sex_encoded'] = df_clean['Sex'].map({'male': 0, 'female': 1})
        df_clean['Embarked_encoded'] = df_clean['Embarked'].map({'S': 0, 'C': 1, 'Q': 2})
        
        app_logger.info("Limpieza de datos completada con éxito.")
        return df_clean
