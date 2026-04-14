import pandas as pd
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from config import config
from utils import app_logger

class TransformationTracker:
    """Tracks and logs all data transformations for audit and visualization."""
    
    def __init__(self, log_path: str = str(config.TRANSFORMATIONS_LOG)):
        self.log_path = log_path
        self._history: List[Dict[str, Any]] = []
        
        # Initialize log file with headers if empty
        with open(self.log_path, "a", encoding="utf-8") as f:
            pass

    def log(self, 
            name: str, 
            columns_affected: List[str], 
            df_before: pd.DataFrame, 
            df_after: pd.DataFrame, 
            description: str = ""):
        """Records a transformation step."""
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "transformation": name,
            "description": description,
            "columns": columns_affected,
            "rows_before": len(df_before),
            "rows_after": len(df_after),
            "stats_diff": self._get_stats_diff(df_before, df_after, columns_affected)
        }
        
        self._history.append(entry)
        
        # Write to log file
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
            
        app_logger.info(f"Transformation tracked: {name}")

    def _get_stats_diff(self, df1: pd.DataFrame, df2: pd.DataFrame, cols: List[str]) -> Dict[str, Any]:
        """Calculates differences in basic stats for affected columns."""
        diff = {}
        for col in cols:
            if col in df1.columns and col in df2.columns:
                if pd.api.types.is_numeric_dtype(df1[col]):
                    diff[col] = {
                        "nulls_before": int(df1[col].isna().sum()),
                        "nulls_after": int(df2[col].isna().sum()),
                        "mean_before": round(float(df1[col].mean()), 2) if not df1[col].empty else 0,
                        "mean_after": round(float(df2[col].mean()), 2) if not df2[col].empty else 0
                    }
        return diff

    def get_history(self) -> List[Dict[str, Any]]:
        """Returns the transformation history."""
        return self._history

tracker = TransformationTracker()
