import logging
import sys
from datetime import datetime
from typing import Any, Dict
from config import config

def setup_logger(name: str) -> logging.Logger:
    """Configures and returns a logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    # File handler for transformations specifically is handled in tracking.py
    # But a general app log could go here if needed.
    
    return logger

def format_timestamp() -> str:
    """Returns a formatted current timestamp."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

app_logger = setup_logger("TitanicApp")
