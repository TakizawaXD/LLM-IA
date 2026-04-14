import pandas as pd
from typing import Dict, Any

class DataStatistics:
    """Calculates advanced metrics and summaries for the dataset."""
    
    @staticmethod
    def get_full_stats(df: pd.DataFrame) -> Dict[str, Any]:
        """Returns comprehensive statistics for EDA."""
        stats = {
            "shape": df.shape,
            "describe": df.describe().to_dict(),
            "survival_rate": float(df['Survived'].mean()),
            "survival_by_sex": df.groupby('Sex')['Survived'].mean().to_dict(),
            "survival_by_class": df.groupby('Pclass')['Survived'].mean().to_dict(),
            "avg_age": float(df['Age'].mean()),
            "avg_fare": float(df['Fare'].mean()),
            "missing_values": df.isna().sum().to_dict()
        }
        return stats

    @staticmethod
    def get_narrative_stats(df: pd.DataFrame) -> str:
        """Genera un resumen textual para que el LLM lo procese."""
        surv_rate = df['Survived'].mean() * 100
        male_surv = df[df['Sex'] == 'male']['Survived'].mean() * 100
        female_surv = df[df['Sex'] == 'female']['Survived'].mean() * 100
        
        summary = (
            f"El dataset del Titanic contiene {len(df)} pasajeros. "
            f"La tasa de supervivencia general fue del {surv_rate:.1f}%. "
            f"La tasa de supervivencia para mujeres fue del {female_surv:.1f}%, mientras que para los hombres fue del {male_surv:.1f}%. "
            f"La edad promedio era de {df['Age'].mean():.1f} años. "
            f"La mayoría de los pasajeros viajaron en la clase {df['Pclass'].mode()[0]}. "
        )
        return summary
