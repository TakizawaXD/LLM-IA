import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from config import config
from utils import app_logger

class ModelTrainer:
    """Trains and evaluates Machine Learning models for survival prediction."""

    def __init__(self):
        self.best_model = None
        self.metrics = {}
        self.feature_importance = None

    def train(self, df: pd.DataFrame):
        """Prepares data, trains multiple models, and selects the best one."""
        # Features to use
        features = ['Pclass', 'Age', 'SibSp', 'Parch', 'Fare', 'FamilySize', 'IsAlone', 'Sex_encoded', 'Embarked_encoded']
        X = df[features]
        y = df['Survived']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # 1. Random Forest
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        rf.fit(X_train, y_train)
        rf_preds = rf.predict(X_test)
        
        # 2. Logistic Regression
        lr = LogisticRegression(max_iter=500)
        lr.fit(X_train, y_train)
        lr_preds = lr.predict(X_test)
        
        # Evaluation
        self.metrics = {
            "RandomForest": self._get_metrics(y_test, rf_preds),
            "LogisticRegression": self._get_metrics(y_test, lr_preds)
        }
        
        # Select best based on F1-score
        if self.metrics["RandomForest"]["f1"] >= self.metrics["LogisticRegression"]["f1"]:
            self.best_model = rf
            self.model_type = "RandomForest"
        else:
            self.best_model = lr
            self.model_type = "LogisticRegression"
            
        # Feature Importance (only for RF)
        if hasattr(self.best_model, 'feature_importances_'):
            self.feature_importance = pd.Series(
                self.best_model.feature_importances_, 
                index=features
            ).sort_values(ascending=False).to_dict()
            
        # Save metrics
        with open(config.METRICS_PATH, 'w') as f:
            json.dump(self.metrics, f, indent=4)
            
        app_logger.info(f"Model training complete. Best model: {self.model_type} with F1={self.metrics[self.model_type]['f1']:.2f}")
        return self.metrics

    def _get_metrics(self, y_true, y_pred) -> dict:
        cm = confusion_matrix(y_true, y_pred)
        return {
            "accuracy": round(accuracy_score(y_true, y_pred), 4),
            "precision": round(precision_score(y_true, y_pred, zero_division=0), 4),
            "recall": round(recall_score(y_true, y_pred), 4),
            "f1": round(f1_score(y_true, y_pred), 4),
            "confusion_matrix": cm.tolist()
        }

    def predict(self, input_data: pd.DataFrame):
        """Predicts survival for new data."""
        if not self.best_model:
            raise ValueError("Model not trained yet.")
        return self.best_model.predict(input_data)
