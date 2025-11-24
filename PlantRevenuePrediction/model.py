import os
from typing import Dict, List, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
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

    def generate_unified_sugarcane_data(self, num_samples: int = 500) -> pd.DataFrame:
        """Generate realistic unified dataset for sugar cane plant decision making.

        This dataset models the SAME sugar cane raw material that can be processed
        into either sugar OR ethanol, with shared plantation conditions.
        """
        np.random.seed(42)
        data = {}
        
        # Generate date range (daily data for past num_samples days)
        end_date = pd.Timestamp.now()
        start_date = end_date - pd.Timedelta(days=num_samples-1)
        data["date"] = pd.date_range(start=start_date, end=end_date, periods=num_samples)
        
        # ========== SHARED BASE FACTORS (Same raw material - sugar cane) ==========
        # Plantation yield and quality (THIS IS THE SAME FOR BOTH PRODUCTS)
        data["cane_yield_tons_per_hectare"] = np.random.normal(80, 15, num_samples)
        data["cane_yield_tons_per_hectare"] = np.clip(data["cane_yield_tons_per_hectare"], 40, 120)

        # Sugar content in cane (Brix) - determines both sugar and ethanol potential
        data["sugar_content_brix"] = np.random.normal(14, 2, num_samples)
        data["sugar_content_brix"] = np.clip(data["sugar_content_brix"], 10, 18)

        # CCS Quality (Commercial Cane Sugar) - affects both products
        data["ccs_quality"] = np.random.normal(11.5, 1.0, num_samples)
        data["ccs_quality"] = np.clip(data["ccs_quality"], 9.0, 14.0)

        # Weather conditions (affects raw material quality)
        data["avg_temp_plantation"] = np.random.normal(26, 3, num_samples)
        data["rainfall_mm"] = np.random.normal(1200, 250, num_samples)
        data["rainfall_mm"] = np.clip(data["rainfall_mm"], 600, 2000)

        # Seasonal factors
        months = np.random.choice(range(1, 13), num_samples)
        data["harvest_month"] = months

        # Plantation costs (fixed - same for both products)
        data["plantation_cost_per_hectare"] = np.random.normal(2000, 300, num_samples)

        # ========== MARKET PRICES (External factors) ==========
        data["sugar_price_per_kg"] = np.random.uniform(0.40, 0.60, num_samples)
        data["ethanol_price_per_liter"] = np.random.uniform(0.50, 0.85, num_samples)
        data["crude_oil_price"] = np.random.uniform(60, 100, num_samples)
        data["gasoline_price"] = np.random.uniform(2.0, 3.2, num_samples)

        # Byproduct values
        data["bagasse_value_per_ton"] = np.random.uniform(15, 35, num_samples)
        data["molasses_value_per_ton"] = np.random.uniform(80, 150, num_samples)

        # ========== PROCESSING COSTS ==========
        data["sugar_processing_cost_per_ton_cane"] = np.random.normal(45, 8, num_samples)
        data["ethanol_processing_cost_per_ton_cane"] = np.random.normal(65, 12, num_samples)
        data["fermentation_efficiency"] = np.random.uniform(0.88, 0.96, num_samples)

        df = pd.DataFrame(data)

        # ========== CALCULATE PRODUCTION YIELDS ==========
        # Sugar production: Extract sugar from cane
        df["sugar_tons_per_hectare"] = df["cane_yield_tons_per_hectare"] * (df["sugar_content_brix"] / 100) * 0.85  # 85% extraction efficiency

        # Ethanol production: Ferment sugar content to ethanol
        # ~70-80 liters ethanol per ton of cane (depends on sugar content and efficiency)
        df["ethanol_liters_per_hectare"] = (
            df["cane_yield_tons_per_hectare"] *
            (df["sugar_content_brix"] / 100) *
            df["fermentation_efficiency"] *
            650  # ~650 liters per ton of fermentable sugar
        )

        # Byproduct yields (available for both, but more bagasse from sugar production)
        df["bagasse_tons_per_hectare"] = df["cane_yield_tons_per_hectare"] * 0.28  # ~28% of cane is bagasse
        df["molasses_tons_per_hectare_sugar"] = df["cane_yield_tons_per_hectare"] * 0.04  # Only from sugar production

        # ========== WEATHER IMPACT ==========
        # Optimal conditions: 24-28°C, 1200mm rainfall
        df["weather_penalty"] = 0
        df["weather_penalty"] += np.clip(np.abs(df["avg_temp_plantation"] - 26) * 2, 0, 15)
        df["weather_penalty"] += np.clip(np.abs(df["rainfall_mm"] - 1200) * 0.01, 0, 10)

        # ========== SCENARIO 1: SUGAR PRODUCTION ==========
        df["sugar_revenue"] = df["sugar_tons_per_hectare"] * df["sugar_price_per_kg"] * 1000  # Convert kg to tons
        df["sugar_byproduct_revenue"] = (
            df["bagasse_tons_per_hectare"] * df["bagasse_value_per_ton"] +
            df["molasses_tons_per_hectare_sugar"] * df["molasses_value_per_ton"]
        )
        df["sugar_processing_cost"] = df["cane_yield_tons_per_hectare"] * df["sugar_processing_cost_per_ton_cane"]
        df["sugar_profit_per_hectare"] = (
            df["sugar_revenue"] +
            df["sugar_byproduct_revenue"] -
            df["sugar_processing_cost"] -
            df["plantation_cost_per_hectare"] -
            df["weather_penalty"]
        )

        # ========== SCENARIO 2: ETHANOL PRODUCTION ==========
        df["ethanol_revenue"] = df["ethanol_liters_per_hectare"] * df["ethanol_price_per_liter"]

        # Ethanol production also produces bagasse (for energy/sale)
        df["ethanol_byproduct_revenue"] = df["bagasse_tons_per_hectare"] * df["bagasse_value_per_ton"]

        df["ethanol_processing_cost"] = df["cane_yield_tons_per_hectare"] * df["ethanol_processing_cost_per_ton_cane"]
        df["ethanol_profit_per_hectare"] = (
            df["ethanol_revenue"] +
            df["ethanol_byproduct_revenue"] -
            df["ethanol_processing_cost"] -
            df["plantation_cost_per_hectare"] -
            df["weather_penalty"]
        )

        # ========== DECISION METRICS ==========
        df["profit_difference"] = df["ethanol_profit_per_hectare"] - df["sugar_profit_per_hectare"]
        df["optimal_strategy"] = df["profit_difference"].apply(
            lambda x: "ethanol" if x > 500 else ("sugar" if x < -500 else "mixed")
        )

        # Add realistic noise
        df["sugar_profit_per_hectare"] *= np.random.normal(1, 0.08, num_samples)
        df["ethanol_profit_per_hectare"] *= np.random.normal(1, 0.08, num_samples)

        # Calculate per-ton and per-liter metrics for UI display
        df["target_net_profit_per_ton"] = df["sugar_profit_per_hectare"] / df["cane_yield_tons_per_hectare"]
        df["target_ethanol_profit_per_liter"] = df["ethanol_profit_per_hectare"] / df["ethanol_liters_per_hectare"]

        return df.round(2)

    def generate_synthetic_data_sugar(self, num_samples: int = 500) -> pd.DataFrame:
        """Generates synthetic dataset for sugar production view.

        Uses the unified dataset but focuses on sugar-relevant features.
        """
        df = self.generate_unified_sugarcane_data(num_samples)

        # Select sugar-focused columns for backward compatibility
        sugar_cols = [
            "date", "sugar_price_per_kg", "ethanol_price_per_liter",
            "bagasse_value_per_ton", "molasses_value_per_ton",
            "avg_temp_plantation", "rainfall_mm", "ccs_quality", "harvest_month",
            "cane_yield_tons_per_hectare", "sugar_content_brix",
            "sugar_profit_per_hectare", "target_net_profit_per_ton"
        ]

        # Rename for UI compatibility
        df_sugar = df[sugar_cols].copy()
        df_sugar = df_sugar.rename(columns={
            "sugar_price_per_kg": "sugar_price",
            "ethanol_price_per_liter": "ethanol_price",
            "bagasse_value_per_ton": "bagasse_value",
            "molasses_value_per_ton": "molasses_value",
            "rainfall_mm": "rainfall_harvest"
        })

        # Scale sugar_price to match UI expectations ($/ton instead of $/kg)
        df_sugar["sugar_price"] = df_sugar["sugar_price"] * 1000

        return df_sugar.round(2)

    def _prepare_features(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        df_encoded = pd.get_dummies(df, columns=["harvest_month"], prefix="month")
        X = df_encoded.drop(
            columns=[
                "date",  # Exclude date column from features
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
    
    def _prepare_ethanol_features(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """Prepare features for ethanol profit prediction."""
        df_encoded = pd.get_dummies(df, columns=["harvest_month"], prefix="month")
        X = df_encoded.drop(
            columns=[
                "date",  # Exclude date column from features
                "target_ethanol_profit_per_liter",
                "ethanol_production_profit",
                "energy_cost_factor",
                "market_correlation",
                "weather_impact",
            ],
            errors="ignore",
        )
        y = df_encoded["target_ethanol_profit_per_liter"]
        return X, y

    def generate_synthetic_data_etanol(self, num_samples: int = 500) -> pd.DataFrame:
        """Generates synthetic dataset for ethanol production view.

        Uses the unified dataset but focuses on ethanol-relevant features.
        This ensures sugar and ethanol datasets share the SAME raw material base.
        """
        df = self.generate_unified_sugarcane_data(num_samples)

        # Select ethanol-focused columns
        ethanol_cols = [
            "date", "ethanol_price_per_liter", "crude_oil_price", "gasoline_price",
            "ccs_quality", "fermentation_efficiency", "harvest_month",
            "cane_yield_tons_per_hectare", "sugar_content_brix",
            "avg_temp_plantation", "rainfall_mm",
            "ethanol_profit_per_hectare", "target_ethanol_profit_per_liter"
        ]

        # Rename for UI compatibility
        df_ethanol = df[ethanol_cols].copy()
        df_ethanol = df_ethanol.rename(columns={
            "ethanol_price_per_liter": "ethanol_price",
            "rainfall_mm": "rainfall_harvest"
        })

        return df_ethanol.round(4)


    def train(self, num_samples: int = 5000, n_estimators: int = 100, max_depth: int = 10) -> Dict:
        """Train the RandomForest model on synthetic data and persist the artifact.

        Returns a dict with metrics and artifact info.
        """
        print("Generating synthetic data for training...")
        df = self.generate_synthetic_data_sugar(num_samples=num_samples)
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

    def train_linear_regression(self, num_samples: int = 5000) -> Dict:
        """Train a Linear Regression model for sugar profit prediction.
        
        This is a simpler, more interpretable alternative to RandomForest.
        Returns a dict with comprehensive metrics and artifact info.
        """
        print("=" * 60)
        print("Training Linear Regression Model for Sugar Profit Prediction")
        print("=" * 60)
        
        print(f"\nGenerating {num_samples} synthetic sugar data samples...")
        df = self.generate_synthetic_data_sugar(num_samples=num_samples)
        X, y = self._prepare_features(df)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        print(f"Training on {len(X_train)} samples, validating on {len(X_test)} samples")

        # Train Linear Regression model
        print("\nTraining Linear Regression model...")
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Make predictions
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)

        # Calculate comprehensive metrics
        # Test set metrics
        mse_test = float(mean_squared_error(y_test, y_pred_test))
        rmse_test = float(np.sqrt(mse_test))
        mae_test = float(mean_absolute_error(y_test, y_pred_test))
        r2_test = float(r2_score(y_test, y_pred_test))
        
        # Train set metrics (to check for overfitting)
        mse_train = float(mean_squared_error(y_train, y_pred_train))
        r2_train = float(r2_score(y_train, y_pred_train))

        # Persist model and feature columns together
        os.makedirs(os.path.dirname(self.model_path) or ".", exist_ok=True)
        artifact = {"model": model, "columns": X.columns.tolist()}
        joblib.dump(artifact, self.model_path)

        self.model = model
        self.feature_columns = X.columns.tolist()

        # Print results
        print("\n" + "=" * 60)
        print("Training Complete!")
        print("=" * 60)
        print(f"Model saved to: {self.model_path}")
        print(f"\nTest Set Performance:")
        print(f"  R² Score:  {r2_test:.4f} (higher is better, 1.0 = perfect)")
        print(f"  MSE:       {mse_test:.2f}")
        print(f"  RMSE:      {rmse_test:.2f}")
        print(f"  MAE:       {mae_test:.2f}")
        print(f"\nTrain Set Performance:")
        print(f"  R² Score:  {r2_train:.4f}")
        print(f"  MSE:       {mse_train:.2f}")
        
        # Check for overfitting
        if r2_train - r2_test > 0.1:
            print(f"\n⚠️  Warning: Possible overfitting detected")
            print(f"   (Train R² - Test R² = {r2_train - r2_test:.4f})")
        else:
            print(f"\n✓ Good generalization (Train R² - Test R² = {r2_train - r2_test:.4f})")
        
        print("=" * 60)

        return {
            "model_path": self.model_path,
            "model_type": "LinearRegression",
            "mse_test": mse_test,
            "rmse_test": rmse_test,
            "mae_test": mae_test,
            "r2_test": r2_test,
            "r2_train": r2_train,
            "n_train": len(X_train),
            "n_test": len(X_test),
            "n_features": X.shape[1],
        }

    def train_linear_regression_ethanol(self, num_samples: int = 5000) -> Dict:
        """Train a Linear Regression model for ethanol profit prediction.

        Returns a dict with comprehensive metrics and artifact info.
        """
        print("=" * 60)
        print("Training Linear Regression Model for Ethanol Profit Prediction")
        print("=" * 60)

        print(f"\nGenerating {num_samples} synthetic ethanol data samples...")
        df = self.generate_synthetic_data_etanol(num_samples=num_samples)
        X, y = self._prepare_ethanol_features(df)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        print(f"Training on {len(X_train)} samples, validating on {len(X_test)} samples")

        # Train Linear Regression model
        print("\nTraining Linear Regression model for ethanol...")
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Make predictions
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)

        # Calculate comprehensive metrics
        # Test set metrics
        mse_test = float(mean_squared_error(y_test, y_pred_test))
        rmse_test = float(np.sqrt(mse_test))
        mae_test = float(mean_absolute_error(y_test, y_pred_test))
        r2_test = float(r2_score(y_test, y_pred_test))

        # Train set metrics (to check for overfitting)
        mse_train = float(mean_squared_error(y_train, y_pred_train))
        r2_train = float(r2_score(y_train, y_pred_train))

        # Persist model and feature columns together
        os.makedirs(os.path.dirname(self.model_path) or ".", exist_ok=True)
        artifact = {"model": model, "columns": X.columns.tolist()}
        joblib.dump(artifact, self.model_path)

        self.model = model
        self.feature_columns = X.columns.tolist()

        # Print results
        print("\n" + "=" * 60)
        print("Ethanol Training Complete!")
        print("=" * 60)
        print(f"Model saved to: {self.model_path}")
        print(f"\nTest Set Performance:")
        print(f"  R² Score:  {r2_test:.4f} (higher is better, 1.0 = perfect)")
        print(f"  MSE:       {mse_test:.2f}")
        print(f"  RMSE:      {rmse_test:.2f}")
        print(f"  MAE:       {mae_test:.2f}")
        print(f"\nTrain Set Performance:")
        print(f"  R² Score:  {r2_train:.4f}")
        print(f"  MSE:       {mse_train:.2f}")

        # Check for overfitting
        if r2_train - r2_test > 0.1:
            print(f"\n⚠️  Warning: Possible overfitting detected")
            print(f"   (Train R² - Test R² = {r2_train - r2_test:.4f})")
        else:
            print(f"\n✓ Good generalization (Train R² - Test R² = {r2_train - r2_test:.4f})")

        print("=" * 60)

        return {
            "model_path": self.model_path,
            "model_type": "LinearRegression_Ethanol",
            "mse_test": mse_test,
            "rmse_test": rmse_test,
            "mae_test": mae_test,
            "r2_test": r2_test,
            "r2_train": r2_train,
            "n_train": len(X_train),
            "n_test": len(X_test),
            "n_features": X.shape[1],
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

    def predict_ethanol(self, input_dict: Dict) -> float:
        """Predict ethanol profit per liter for a single scenario.

        input_dict should contain ethanol feature keys, e.g.:
        ethanol_price, crude_oil_price, gasoline_price, ccs_quality,
        fermentation_efficiency, harvest_month.
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
        df = self.generate_synthetic_data_sugar(num_samples=num_samples)
        X, y = self._prepare_features(df)
        if self.model is None:
            self.load()
        preds = self.model.predict(X)
        return {"mse": float(mean_squared_error(y, preds)), "r2": float(r2_score(y, preds))}

    def evaluate_ethanol_on_generated(self, num_samples: int = 2000) -> Dict:
        """Generate an ethanol dataset and evaluate the saved model on it."""
        df = self.generate_synthetic_data_etanol(num_samples=num_samples)
        X, y = self._prepare_ethanol_features(df)
        if self.model is None:
            self.load()
        preds = self.model.predict(X)
        return {"mse": float(mean_squared_error(y, preds)), "r2": float(r2_score(y, preds))}

    def predict_optimal_production(self, conditions: Dict) -> Dict:
        """Predict whether to focus on sugar or ethanol production.

        Args:
            conditions: Dict with plantation conditions and market prices:
                - cane_yield_tons_per_hectare
                - sugar_content_brix
                - ccs_quality
                - avg_temp_plantation
                - rainfall_mm
                - harvest_month
                - sugar_price_per_kg
                - ethanol_price_per_liter
                - fermentation_efficiency
                - plantation_cost_per_hectare
                - sugar_processing_cost_per_ton_cane
                - ethanol_processing_cost_per_ton_cane
                - bagasse_value_per_ton
                - molasses_value_per_ton

        Returns:
            Dict with recommendation, profit estimates, and reasoning
        """
        # Calculate sugar production scenario
        sugar_tons = conditions["cane_yield_tons_per_hectare"] * (conditions["sugar_content_brix"] / 100) * 0.85
        sugar_revenue = sugar_tons * conditions["sugar_price_per_kg"] * 1000
        bagasse_tons = conditions["cane_yield_tons_per_hectare"] * 0.28
        molasses_tons = conditions["cane_yield_tons_per_hectare"] * 0.04
        sugar_byproduct = (bagasse_tons * conditions["bagasse_value_per_ton"] +
                          molasses_tons * conditions["molasses_value_per_ton"])
        sugar_processing = conditions["cane_yield_tons_per_hectare"] * conditions["sugar_processing_cost_per_ton_cane"]

        weather_penalty = 0
        weather_penalty += abs(conditions["avg_temp_plantation"] - 26) * 2
        weather_penalty += abs(conditions.get("rainfall_mm", 1200) - 1200) * 0.01

        sugar_profit = (sugar_revenue + sugar_byproduct - sugar_processing -
                       conditions["plantation_cost_per_hectare"] - weather_penalty)

        # Calculate ethanol production scenario
        ethanol_liters = (conditions["cane_yield_tons_per_hectare"] *
                         (conditions["sugar_content_brix"] / 100) *
                         conditions["fermentation_efficiency"] * 650)
        ethanol_revenue = ethanol_liters * conditions["ethanol_price_per_liter"]
        ethanol_byproduct = bagasse_tons * conditions["bagasse_value_per_ton"]
        ethanol_processing = conditions["cane_yield_tons_per_hectare"] * conditions["ethanol_processing_cost_per_ton_cane"]

        ethanol_profit = (ethanol_revenue + ethanol_byproduct - ethanol_processing -
                         conditions["plantation_cost_per_hectare"] - weather_penalty)

        # Decision logic
        profit_diff = ethanol_profit - sugar_profit
        confidence = min(abs(profit_diff) / 2000, 1.0)

        if profit_diff > 500:
            recommendation = "ethanol"
            reasoning = f"Ethanol production is ${profit_diff:.0f} more profitable per hectare. Focus on ethanol."
        elif profit_diff < -500:
            recommendation = "sugar"
            reasoning = f"Sugar production is ${abs(profit_diff):.0f} more profitable per hectare. Focus on sugar."
        else:
            recommendation = "mixed"
            reasoning = f"Profits are similar (difference: ${abs(profit_diff):.0f}). Consider mixed production strategy."

        return {
            "recommendation": recommendation,
            "sugar_profit_per_hectare": round(sugar_profit, 2),
            "ethanol_profit_per_hectare": round(ethanol_profit, 2),
            "profit_difference": round(profit_diff, 2),
            "confidence": round(confidence, 2),
            "reasoning": reasoning,
            "sugar_production_liters": 0,
            "sugar_production_tons": round(sugar_tons, 2),
            "ethanol_production_liters": round(ethanol_liters, 2),
            "byproduct_revenue_sugar": round(sugar_byproduct, 2),
            "byproduct_revenue_ethanol": round(ethanol_byproduct, 2)
        }

