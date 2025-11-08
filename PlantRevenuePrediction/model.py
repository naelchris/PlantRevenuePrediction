# ...new file...
import os
from typing import Dict, List, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


class SugarcaneModel:
    """Object-oriented ML pipeline for sugarcane revenue prediction.

    Responsibilities:
    - Generate synthetic training data (replace with real data loading in prod).
    - Train a RandomForestRegressor and persist the model and feature columns.
    - Load a saved model and predict for single scenarios.
    """

    DEFAULT_MODEL_PATH = "models/revenue_model.joblib"

    def __init__(self, model_path: str = DEFAULT_MODEL_PATH):
        self.model_path = model_path
        self.model = None
        self.feature_columns: List[str] = []

    def generate_synthetic_data(self, num_samples: int = 500) -> pd.DataFrame:
        """Generates synthetic dataset similar to the provided script.

        Replace this with a proper data loader when real historical data is available.
        """
        np.random.seed(42)
        data = {}
        data["sugar_price"] = np.random.uniform(650, 850, num_samples)
        data["ethanol_price"] = np.random.uniform(0.40, 0.70, num_samples)
        data["bagasse_value"] = np.random.uniform(15, 30, num_samples)
        data["molasses_value"] = np.random.uniform(5, 12, num_samples)
        data["avg_temp_plantation"] = np.random.normal(25, 2, num_samples)
        data["rainfall_harvest"] = np.random.normal(150, 50, num_samples)
        data["ccs_quality"] = np.random.normal(11.5, 1.0, num_samples)
        data["ccs_quality"] = np.clip(data["ccs_quality"], 9.0, 14.0)
        months = np.random.choice(range(1, 13), num_samples)
        data["harvest_month"] = months

        df = pd.DataFrame(data)

        df["base_sugar_profit"] = (df["sugar_price"] * df["ccs_quality"] / 11.5) * 0.10
        df["ethanol_profit"] = df["ethanol_price"] * 85.0 * (df["ccs_quality"] / 11.5) * 0.75
        df["side_product_profit"] = df["bagasse_value"] * 0.05 + df["molasses_value"] * 0.03
        df["weather_penalty"] = np.clip((df["rainfall_harvest"] - 200) * 0.05, 0, 10)
        df["weather_penalty"] += np.clip(np.abs(df["avg_temp_plantation"] - 28) * 0.5, 0, 5)

        df["target_net_profit_per_ton"] = (
            (df["base_sugar_profit"] * 0.4)
            + (df["ethanol_profit"] * 0.6)
            + df["side_product_profit"]
            - df["weather_penalty"]
            - 50.0
        )

        df["target_net_profit_per_ton"] = df["target_net_profit_per_ton"] * np.random.normal(1, 0.05, num_samples)

        return df.round(2)

    def _prepare_features(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        df_encoded = pd.get_dummies(df, columns=["harvest_month"], prefix="month")
        X = df_encoded.drop(
            columns=[
                "target_net_profit_per_ton",
                "base_sugar_profit",
                "ethanol_profit",
                "side_product_profit",
                "weather_penalty",
            ],
            errors="ignore",
        )
        y = df_encoded["target_net_profit_per_ton"]
        return X, y

    def train(self, num_samples: int = 5000, n_estimators: int = 100, max_depth: int = 10) -> Dict:
        """Train the RandomForest model on synthetic data and persist the artifact.

        Returns a dict with metrics and artifact info.
        """
        print("Generating synthetic data for training...")
        df = self.generate_synthetic_data(num_samples=num_samples)
        X, y = self._prepare_features(df)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        print(f"Training on {len(X_train)} samples, validating on {len(X_test)} samples")

        model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        mse = float(mean_squared_error(y_test, y_pred))
        r2 = float(r2_score(y_test, y_pred))

        # Persist model and feature columns together so we can align during prediction
        os.makedirs(os.path.dirname(self.model_path) or ".", exist_ok=True)
        artifact = {"model": model, "columns": X.columns.tolist()}
        joblib.dump(artifact, self.model_path)

        self.model = model
        self.feature_columns = X.columns.tolist()

        print("Model training complete. Saved model to:", self.model_path)
        return {
            "model_path": self.model_path,
            "mse": mse,
            "r2": r2,
            "n_train": len(X_train),
            "n_test": len(X_test),
        }

    def load(self) -> None:
        """Load the persisted model artifact into memory."""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model not found at {self.model_path}")
        artifact = joblib.load(self.model_path)
        self.model = artifact["model"]
        self.feature_columns = artifact.get("columns", [])

    def predict(self, input_dict: Dict) -> float:
        """Predict a single scenario input_dict and return predicted profit per ton.

        input_dict should contain the base feature keys used in training, e.g.
        sugar_price, ethanol_price, bagasse_value, molasses_value,
        avg_temp_plantation, rainfall_harvest, ccs_quality, harvest_month.
        """
        if self.model is None:
            self.load()

        # Build a DataFrame from the input dict and one-hot encode month columns
        new_df = pd.DataFrame([input_dict])
        for month in range(1, 13):
            col = f"month_{month}"
            new_df[col] = 0
        # If harvest_month provided, set its column
        if "harvest_month" in input_dict:
            new_df[f"month_{int(input_dict['harvest_month'])}"] = 1

        # Align to training columns
        X_new = new_df.reindex(columns=self.feature_columns, fill_value=0)

        pred = float(self.model.predict(X_new)[0])
        return pred

    def evaluate_on_generated(self, num_samples: int = 2000) -> Dict:
        """Generate a dataset and evaluate the saved model on it (useful smoke test)."""
        df = self.generate_synthetic_data(num_samples=num_samples)
        X, y = self._prepare_features(df)
        if self.model is None:
            self.load()
        preds = self.model.predict(X)
        return {"mse": float(mean_squared_error(y, preds)), "r2": float(r2_score(y, preds))}

