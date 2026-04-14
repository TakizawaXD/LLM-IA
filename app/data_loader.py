import pandas as pd
import requests
import io
from typing import Optional
from config import config
from utils import app_logger

class DataLoader:
    """Handles data ingestion from local sources or remote URLs."""
    
    REMOTE_URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

    @staticmethod
    def load_data(file_path: Optional[str] = None) -> pd.DataFrame:
        """Loads the Titanic dataset. Prioritizes SQLite, then Local CSV, then Remote."""
        from database import db_manager
        
        # 1. Try loading from Database
        df = db_manager.load_table("passengers_raw")
        if not df.empty:
            app_logger.info("Loaded data from SQLite database.")
            return df
            
        # 2. Try loading from Local CSV and sync to DB
        path = file_path or str(config.RAW_DATA_PATH)
        if config.RAW_DATA_PATH.exists():
            app_logger.info(f"Loading local CSV from {path}")
            df = pd.read_csv(path)
            db_manager.save_dataframe(df, "passengers_raw")
            return df
            
        # 3. Download from Remote, save CSV, and sync to DB
        try:
            app_logger.info("Data not found locally. Downloading from remote repository...")
            response = requests.get(DataLoader.REMOTE_URL)
            response.raise_for_status()
            df = pd.read_csv(io.StringIO(response.text))
            
            # Save files and sync
            config.DATA_DIR.mkdir(parents=True, exist_ok=True)
            df.to_csv(config.RAW_DATA_PATH, index=False)
            db_manager.save_dataframe(df, "passengers_raw")
            
            app_logger.info("Data downloaded, saved to CSV and synced to SQLite.")
            return df
        except Exception as e:
            app_logger.error(f"Error loading data: {e}")
            raise e

    @staticmethod
    def get_summary(df: pd.DataFrame) -> dict:
        """Returns a basic summary of the dataframe."""
        return {
            "rows": df.shape[0],
            "cols": df.shape[1],
            "columns": list(df.columns),
            "types": df.dtypes.apply(lambda x: str(x)).to_dict(),
            "nulls": df.isna().sum().to_dict(),
            "duplicates": int(df.duplicated().sum())
        }
