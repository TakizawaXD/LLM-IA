import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Any

# Set visual style
sns.set_theme(style="darkgrid", palette="muted")
plt.rcParams['figure.figsize'] = (10, 6)

class Visualizer:
    """Generates professional plots for Data Science reports and Streamlit."""

    @staticmethod
    def plot_nulls_heatmap(df: pd.DataFrame):
        """Fase 1: Mapa de calor de valores nulos."""
        plt.figure(figsize=(10, 6))
        sns.heatmap(df.isnull(), yticklabels=False, cbar=False, cmap='viridis')
        plt.title("Mapa de Datos Faltantes")
        return plt

    @staticmethod
    def plot_correlation_matrix(df: pd.DataFrame):
        """Fase 1: Matriz de correlación."""
        numeric_df = df.select_dtypes(include=['number'])
        plt.figure(figsize=(10, 8))
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
        plt.title("Mapa de Correlación de Variables")
        return plt

    @staticmethod
    def plot_survival_by_sex(df: pd.DataFrame):
        fig = px.bar(df.groupby('Sex')['Survived'].mean().reset_index(), 
                     x='Sex', y='Survived', color='Sex',
                     title="Probabilidad de Supervivencia por Género",
                     labels={'Survived': 'Tasa de Supervivencia', 'Sex': 'Género'})
        return fig

    @staticmethod
    def plot_survival_by_class(df: pd.DataFrame):
        fig = px.sunburst(df, path=['Pclass', 'Sex'], values='Survived',
                          title="Distribución de Supervivencia por Clase y Género",
                          labels={'Survived': 'Supervivientes', 'Pclass': 'Clase', 'Sex': 'Género'})
        return fig

    @staticmethod
    def plot_age_distribution(df: pd.DataFrame):
        fig = px.histogram(df, x="Age", color="Survived", marginal="rug",
                           title="Distribución de Edad por Supervivencia",
                           labels={'Age': 'Edad', 'Survived': 'Supervivencia'},
                           nbins=30, barmode="overlay")
        return fig

    @staticmethod
    def plot_fare_by_class_boxplot(df: pd.DataFrame):
        fig = px.box(df, x="Pclass", y="Fare", color="Pclass",
                     title="Distribución de Tarifas por Clase de Pasajero",
                     labels={'Pclass': 'Clase', 'Fare': 'Tarifa'},
                     log_y=True)
        return fig

    @staticmethod
    def plot_interactive_age_survival(df: pd.DataFrame):
        """Fase 4: Dispersión de Supervivencia vs Edad."""
        fig = px.scatter(df, x="Age", y="Fare", color="Survived", size="FamilySize",
                         hover_data=['Name', 'Pclass'],
                         title="Vista Interactiva: Edad vs Tarifa (Color por Supervivencia)",
                         labels={'Age': 'Edad', 'Fare': 'Tarifa', 'Survived': 'Supervivencia', 'FamilySize': 'Tamaño Familia'})
        return fig

    @staticmethod
    def plot_stratified_scatter(df: pd.DataFrame):
        """Gráfica de puntos estratificada inspirada en el layout solicitado."""
        plot_df = df.copy()
        
        # Calculamos dos categorias para copiar exactamente la 'estratificacion' visual de la imagen
        plot_df['Estratificacion_Edad'] = plot_df['Age'].apply(lambda x: 'Mayores de 35 años' if x >= 35 else 'Menores de 35 años')
        
        fig = px.scatter(
            plot_df, 
            x="Fare", 
            y="Age", 
            color="Estratificacion_Edad",
            title="Gráfica de puntos estratificada",
            labels={'Fare': 'Tarifa pagada ($)', 'Age': 'Edad (años)', 'Estratificacion_Edad': ''},
            color_discrete_map={'Menores de 35 años': '#f48c42', 'Mayores de 35 años': '#427bf4'} # Naranja y Azul
        )
        
        fig.update_traces(marker=dict(size=12, opacity=0.85))
        fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)', title_font=dict(size=14))
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)', title_font=dict(size=14))
        
        return fig

    @staticmethod
    def plot_family_survival(df: pd.DataFrame):
        fig = px.line(df.groupby('FamilySize')['Survived'].mean().reset_index(),
                      x='FamilySize', y='Survived', markers=True,
                      title="Impacto del Tamaño de la Familia en la Supervivencia",
                      labels={'FamilySize': 'Tamaño de Familia', 'Survived': 'Tasa de Supervivencia'})
        return fig

    @staticmethod
    def plot_line_with_reference(df: pd.DataFrame):
        """Gráfica de líneas con base rellena (área) y referencia visual horizontal."""
        df_copy = df.copy()
        # Agrupar por edades (cada 5 años) para suavizar la línea
        df_copy['Rango Edad'] = (df_copy['Age'] // 5) * 5
        trend_df = df_copy.groupby('Rango Edad')['Survived'].mean().reset_index()
        
        global_mean = df['Survived'].mean() * 100
        
        fig = go.Figure()

        # Añadir linea base con area rellena ("con base")
        fig.add_trace(go.Scatter(
            x=trend_df['Rango Edad'], 
            y=trend_df['Survived'] * 100,
            mode='lines+markers',
            name='Supervivencia',
            line=dict(shape='spline', color='#00d4ff', width=4), # Spline para curvas bonitas
            marker=dict(size=8, color='#007bb5', symbol='circle'),
            fill='tozeroy', # "Con base" rellena
            fillcolor='rgba(0, 212, 255, 0.15)' 
        ))

        # Referencia visual (Línea promedio)
        fig.add_hline(
            y=global_mean, 
            line_dash="dot", 
            annotation_text=f"Promedio General ({global_mean:.1f}%)", 
            annotation_position="bottom right",
            line_color="#ff4b4b",
            line_width=2
        )

        fig.update_layout(
            title='Tendencia de Supervivencia por Edad (con Referencia)',
            xaxis_title='Rango de Edad (años)',
            yaxis_title='Probabilidad de Sobrevivir (%)',
            plot_bgcolor='rgba(0,0,0,0.25)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            hovermode="x unified",
            margin=dict(l=40, r=40, t=60, b=40)
        )
        
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)', title_font=dict(size=14))
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)', range=[0, 105], title_font=dict(size=14))
        
        return fig

    @staticmethod
    def plot_global_parallel_categories(df: pd.DataFrame):
        """Visualización global de todas las dimensiones clave."""
        # Usar un subconjunto de columnas categóricas significativas
        plot_df = df.copy()
        plot_df['Resultado'] = plot_df['Survived'].map({0: 'Falleció', 1: 'Sobrevivió'})
        
        fig = px.parallel_categories(
            plot_df, 
            dimensions=['Pclass', 'Sex', 'AgeGroup', 'Embarked', 'Resultado'],
            color="Survived", 
            color_continuous_scale=px.colors.sequential.Inferno,
            title="Vista Global: Flujo de Pasajeros e Intersecciones de Supervivencia",
            labels={'Pclass': 'Clase', 'Sex': 'Género', 'AgeGroup': 'Grupo Edad', 'Embarked': 'Puerto', 'Resultado': 'Resultado'}
        )
        fig.update_layout(margin=dict(l=50, r=50, t=80, b=50))
        return fig

    @staticmethod
    def plot_dot_plot(df: pd.DataFrame):
        """Gráfica de puntos (Strip Plot) para visualizar distribución."""
        plot_df = df.copy()
        plot_df['Pclass'] = plot_df['Pclass'].astype(str) # Forzar categoría 1,2,3
        plot_df['Supervivencia_Str'] = plot_df['Survived'].astype(str) # 0 o 1
        
        fig = px.strip(
            plot_df, 
            x="Age", 
            y="Pclass", 
            color="Supervivencia_Str", 
            orientation="h",
            title="Gráfica de Puntos: Distribución de Edad por Clase y Supervivencia",
            labels={'Age': 'Edad', 'Pclass': 'Clase', 'Supervivencia_Str': 'Supervivencia'},
            color_discrete_map={'0': '#ff4b4b', '1': '#00d4ff'} # Rojo coral para fallecido (0), Cyan brillante para sobreviviente (1)
        )
        
        fig.update_traces(marker=dict(size=8, opacity=0.9))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0.25)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        # Activar las lineas de fondo (grid) para mejor lectura de datos manteniendo la estetica
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)', zeroline=False)
        # category descending pone la clase 3 arriba y la 1 abajo, identico a la foto
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.05)', zeroline=False, categoryorder='category descending')
        
        return fig
