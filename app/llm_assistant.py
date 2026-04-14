import requests
import json
from typing import Optional
from config import config
from utils import app_logger

class LLMAssistant:
    """Interfaces with Hugging Face API to provide natural language insights."""

    def __init__(self, api_key: Optional[str] = config.HF_API_KEY, model_id: str = config.MODEL_ID):
        self.api_key = api_key
        self.model_id = model_id
        self.api_url = f"https://api-inference.huggingface.co/models/{model_id}"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def query(self, prompt: str) -> str:
        """Sends a query to the Hugging Face model."""
        if not self.api_key:
            return "Error: Falta la clave de API de Hugging Face. Por favor, revisa tu archivo .env."

        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 250, "temperature": 0.7}
        }
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            # Result format depends on the model (text2text vs text-generation)
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "I couldn't generate a response.")
            return str(result)
            
        except Exception as e:
            app_logger.error(f"Error en API de LLM: {e}")
            return f"Lo siento, tengo problemas para conectarme a mi cerebro en este momento. Error: {str(e)}"

    def analyze_dataset(self, summary_text: str, question: str) -> str:
        """Construye un prompt con contexto para el LLM."""
        prompt = (
            f"Contexto sobre el Dataset del Titanic: {summary_text}\n\n"
            f"Pregunta del Usuario: {question}\n\n"
            f"Responde estrictamente basándote en el contexto anterior. Sé conciso y profesional en español."
        )
        return self.query(prompt)

    def generate_report_summary(self, metrics: dict) -> str:
        """Genera un resumen de los resultados del modelo de ML."""
        prompt = (
            f"Resume estos resultados de machine learning para un informe de negocios:\n"
            f"{json.dumps(metrics, indent=2)}\n\n"
            f"Enfócate en el mejor modelo y qué significan las puntuaciones para la predicción de supervivientes del Titanic. Responde en español."
        )
        return self.query(prompt)
