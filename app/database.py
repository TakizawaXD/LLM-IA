import sqlite3
import pandas as pd
from pathlib import Path
from typing import Optional
from config import config
from utils import app_logger

class DatabaseManager:
    """Manages the local SQLite database for data science persistence."""
    
    def __init__(self, db_path: str = str(config.DATA_DIR / "titanic.db")):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """Creates the database and schema if it doesn't exist."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS simulation_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        age INTEGER,
                        sex TEXT,
                        pclass INTEGER,
                        sibsp INTEGER,
                        parch INTEGER,
                        fare REAL,
                        embarked TEXT,
                        alone TEXT,
                        prediction_outcome INTEGER,
                        survival_probability REAL
                    )
                """)
                conn.commit()
                app_logger.info(f"Database initialized at {self.db_path}")
        except Exception as e:
            app_logger.error(f"DB Initialization Error: {e}")

    def save_dataframe(self, df: pd.DataFrame, table_name: str, if_exists: str = "replace"):
        """Saves a pandas DataFrame to a SQLite table."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                df.to_sql(table_name, conn, if_exists=if_exists, index=False)
                app_logger.info(f"Saved {len(df)} rows to table '{table_name}'")
        except Exception as e:
            app_logger.error(f"Error saving to DB: {e}")

    def log_simulation(self, payload: dict):
        """Logs user interactions from the Simulator directly into DB."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO simulation_logs 
                    (age, sex, pclass, sibsp, parch, fare, embarked, alone, prediction_outcome, survival_probability)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    payload.get('age'), payload.get('sex'), payload.get('pclass'),
                    payload.get('sibsp'), payload.get('parch'), payload.get('fare'),
                    payload.get('embarked'), payload.get('alone'), 
                    payload.get('prediction_outcome'), payload.get('survival_probability')
                ))
                conn.commit()
        except Exception as e:
            app_logger.error(f"Error logging simulation to DB: {e}")

    def load_query(self, query: str) -> pd.DataFrame:
        """Executes a SQL query and returns a DataFrame."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                return pd.read_sql_query(query, conn)
        except Exception as e:
            app_logger.error(f"Error running query: {e}")
            return pd.DataFrame()

    def load_table(self, table_name: str) -> pd.DataFrame:
        """Loads an entire table from the database."""
        return self.load_query(f"SELECT * FROM {table_name}")

db_manager = DatabaseManager()
