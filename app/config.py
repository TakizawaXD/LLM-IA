import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Project configuration management."""
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    REPORTS_DIR = BASE_DIR / "reports"
    
    # Files
    RAW_DATA_PATH = DATA_DIR / "titanic.csv"
    CLEANED_DATA_PATH = REPORTS_DIR / "cleaned_dataset.csv"
    TRANSFORMATIONS_LOG = LOGS_DIR / "transformations.log"
    METRICS_PATH = REPORTS_DIR / "metrics.json"
    REPORT_MD_PATH = REPORTS_DIR / "analysis_report.md"
    
    # API Keys
    HF_API_KEY = os.getenv("HF_API_KEY")
    MODEL_ID = os.getenv("MODEL_ID", "google/flan-t5-base")
    
    # Ensure directories exist
    DATA_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)

config = Config()
