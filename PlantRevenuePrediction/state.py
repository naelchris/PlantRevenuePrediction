import threading
import reflex as rx

class State(rx.State):
    revenue: float = 0.0  # attribute revenue

    # Inputs for prediction
    sugar_price: float = 700.0
    ethanol_price: float = 0.5
    bagasse_value: float = 20.0
    molasses_value: float = 8.0
    avg_temp_plantation: float = 26.0
    rainfall_harvest: float = 150.0
    ccs_quality: float = 11.5
    harvest_month: int = 9

    predicted_profit: float = 0.0
    training_status: str = "idle"
    
    # Training metrics
    training_metrics: dict = {}
    show_training_results: bool = False

    # Data tables for datasets
    sugar_data: list[dict] = []
    ethanol_data: list[dict] = []
    sugar_data_loaded: bool = False
    ethanol_data_loaded: bool = False
    
    # Chart data (larger datasets for visualization)
    sugar_chart_data: list[dict] = []
    ethanol_chart_data: list[dict] = []
    
    # Ethanol-specific variables
    predicted_ethanol_profit: float = 0.0
    ethanol_training_status: str = "idle"
    ethanol_training_metrics: dict = {}
    show_ethanol_training_results: bool = False
    
    # Additional ethanol input parameters
    crude_oil_price: float = 80.0
    gasoline_price: float = 2.5
    fermentation_efficiency: float = 0.90

    # ========== UNIFIED PRODUCTION DECISION VARIABLES ==========
    # Shared plantation conditions (same raw material)
    cane_yield_tons_per_hectare: float = 80.0
    sugar_content_brix: float = 14.0
    plantation_cost_per_hectare: float = 2000.0
    rainfall_mm: float = 1200.0

    # Processing costs
    sugar_processing_cost: float = 45.0
    ethanol_processing_cost: float = 65.0

    # Byproduct prices
    bagasse_value: float = 25.0
    molasses_value: float = 100.0

    # Recalculated prices (per kg/liter for realistic calculations)
    sugar_price_per_kg: float = 0.50
    ethanol_price_per_liter: float = 0.65

    # Decision outputs
    production_recommendation: str = ""
    sugar_profit_per_hectare: float = 0.0
    ethanol_profit_per_hectare: float = 0.0
    profit_difference: float = 0.0
    recommendation_confidence: float = 0.0
    recommendation_reasoning: str = ""
    show_decision_results: bool = False

    # Production yields
    sugar_production_tons: float = 0.0
    ethanol_production_liters: float = 0.0

    def load_revenue(self):
        # we can get from db or api
        self.revenue = 1000000.0
        return self.revenue

    # --- Explicit setters for UI bindings (each receives the raw value from the input) ---
    def set_sugar_price(self, value) -> None:
        try:
            self.sugar_price = float(value)
        except Exception:
            pass

    def set_ethanol_price(self, value) -> None:
        try:
            self.ethanol_price = float(value)
        except Exception:
            pass

    def set_bagasse_value(self, value) -> None:
        try:
            self.bagasse_value = float(value)
        except Exception:
            pass

    def set_molasses_value(self, value) -> None:
        try:
            self.molasses_value = float(value)
        except Exception:
            pass

    def set_avg_temp_plantation(self, value) -> None:
        try:
            self.avg_temp_plantation = float(value)
        except Exception:
            pass

    def set_rainfall_harvest(self, value) -> None:
        try:
            self.rainfall_harvest = float(value)
        except Exception:
            pass

    def set_ccs_quality(self, value) -> None:
        try:
            self.ccs_quality = float(value)
        except Exception:
            pass

    def set_harvest_month(self, value) -> None:
        try:
            # harvest month should be an int between 1 and 12
            m = int(float(value))
            if 1 <= m <= 12:
                self.harvest_month = m
        except Exception:
            pass

    def set_crude_oil_price(self, value) -> None:
        try:
            self.crude_oil_price = float(value)
        except Exception:
            pass

    def set_gasoline_price(self, value) -> None:
        try:
            self.gasoline_price = float(value)
        except Exception:
            pass

    def set_fermentation_efficiency(self, value) -> None:
        try:
            eff = float(value)
            if 0.0 <= eff <= 1.0:
                self.fermentation_efficiency = eff
        except Exception:
            pass

    def set_cane_yield(self, value) -> None:
        try:
            self.cane_yield_tons_per_hectare = float(value)
        except Exception:
            pass

    def set_sugar_content_brix(self, value) -> None:
        try:
            self.sugar_content_brix = float(value)
        except Exception:
            pass

    def set_plantation_cost(self, value) -> None:
        try:
            self.plantation_cost_per_hectare = float(value)
        except Exception:
            pass

    def set_rainfall_mm(self, value) -> None:
        try:
            self.rainfall_mm = float(value)
        except Exception:
            pass

    def set_sugar_processing_cost(self, value) -> None:
        try:
            self.sugar_processing_cost = float(value)
        except Exception:
            pass

    def set_ethanol_processing_cost(self, value) -> None:
        try:
            self.ethanol_processing_cost = float(value)
        except Exception:
            pass

    def predict_optimal_strategy(self) -> None:
        """Calculate which production strategy (sugar vs ethanol) is more profitable."""
        try:
            from .model import SugarcaneModel

            model = SugarcaneModel()

            # Prepare conditions based on current state
            conditions = {
                "cane_yield_tons_per_hectare": self.cane_yield_tons_per_hectare,
                "sugar_content_brix": self.sugar_content_brix,
                "ccs_quality": self.ccs_quality,
                "avg_temp_plantation": self.avg_temp_plantation,
                "rainfall_mm": self.rainfall_mm,
                "harvest_month": self.harvest_month,
                "sugar_price_per_kg": self.sugar_price / 1000,  # Convert back to per kg
                "ethanol_price_per_liter": self.ethanol_price,
                "fermentation_efficiency": self.fermentation_efficiency,
                "plantation_cost_per_hectare": self.plantation_cost_per_hectare,
                "sugar_processing_cost_per_ton_cane": self.sugar_processing_cost,
                "ethanol_processing_cost_per_ton_cane": self.ethanol_processing_cost,
                "bagasse_value_per_ton": self.bagasse_value,
                "molasses_value_per_ton": self.molasses_value,
            }

            result = model.predict_optimal_production(conditions)

            self.production_recommendation = result["recommendation"]
            self.sugar_profit_per_hectare = result["sugar_profit_per_hectare"]
            self.ethanol_profit_per_hectare = result["ethanol_profit_per_hectare"]
            self.profit_difference = result["profit_difference"]
            self.recommendation_confidence = result["confidence"]
            self.recommendation_reasoning = result["reasoning"]
            self.sugar_production_tons = result["sugar_production_tons"]
            self.ethanol_production_liters = result["ethanol_production_liters"]
            self.show_decision_results = True

        except Exception as e:
            print("Decision prediction error:", e)
            self.production_recommendation = "error"
            self.recommendation_reasoning = f"Error calculating recommendation: {str(e)}"
            self.show_decision_results = False

    def predict_profit(self) -> None:
        """Server-side method: load model and predict profit per ton using current state inputs."""
        try:
            from .model import SugarcaneModel

            model = SugarcaneModel()
            inp = {
                "sugar_price": float(self.sugar_price),
                "ethanol_price": float(self.ethanol_price),
                "bagasse_value": float(self.bagasse_value),
                "molasses_value": float(self.molasses_value),
                "avg_temp_plantation": float(self.avg_temp_plantation),
                "rainfall_harvest": float(self.rainfall_harvest),
                "ccs_quality": float(self.ccs_quality),
                "harvest_month": int(self.harvest_month),
            }
            self.predicted_profit = model.predict(inp)
        except Exception as e:
            # Keep UI-friendly state; don't raise here because Reflex will try to serialize exceptions
            self.predicted_profit = 0.0
            print("Prediction error:", e)

    def _run_training_thread(self):
        try:
            self.training_status = "running"
            from .train import main as train_main

            metrics = train_main()
            if metrics:
                self.training_metrics = metrics
                self.show_training_results = True
            self.training_status = "completed"
        except Exception as e:
            self.training_status = "failed"
            self.show_training_results = False
            print("Training error:", e)

    def start_training(self) -> None:
        """Kick off training in a background thread to avoid blocking request handling."""
        thread = threading.Thread(target=self._run_training_thread, daemon=True)
        thread.start()
        self.training_status = "started"

    def predict_ethanol_profit(self) -> None:
        """Predict ethanol profit per liter using current state inputs."""
        try:
            from .model import SugarcaneModel

            model = SugarcaneModel(model_path="models/ethanol_linear_regression.joblib")
            model.load()

            scenario = {
                "ethanol_price": self.ethanol_price,
                "crude_oil_price": self.crude_oil_price,
                "gasoline_price": self.gasoline_price,
                "ccs_quality": self.ccs_quality,
                "fermentation_efficiency": self.fermentation_efficiency,
                "harvest_month": self.harvest_month,
            }
            self.predicted_ethanol_profit = model.predict_ethanol(scenario)
        except Exception as e:
            self.predicted_ethanol_profit = 0.0
            print("Ethanol prediction error:", e)

    def _run_ethanol_training_thread(self):
        try:
            self.ethanol_training_status = "running"
            from .model import SugarcaneModel

            model = SugarcaneModel(model_path="models/ethanol_linear_regression.joblib")
            metrics = model.train_linear_regression_ethanol(num_samples=5000)
            if metrics:
                self.ethanol_training_metrics = metrics
                self.show_ethanol_training_results = True
            self.ethanol_training_status = "completed"
        except Exception as e:
            self.ethanol_training_status = "failed"
            self.show_ethanol_training_results = False
            print("Ethanol training error:", e)

    def start_ethanol_training(self) -> None:
        """Kick off ethanol training in a background thread."""
        thread = threading.Thread(target=self._run_ethanol_training_thread, daemon=True)
        thread.start()
        self.ethanol_training_status = "started"

    def load_sugar_data(self) -> None:
        """Load synthetic sugar dataset for display."""
        try:
            from .model import SugarcaneModel

            model = SugarcaneModel()
            # Generate table data (small sample for table)
            df_table = model.generate_synthetic_data_sugar(num_samples=10)
            
            # Generate chart data (larger sample for charts)
            df_chart = model.generate_synthetic_data_sugar(num_samples=100)

            # Convert table data to list of dicts and limit columns for display
            display_cols = [
                "sugar_price", "ethanol_price", "ccs_quality",
                "avg_temp_plantation", "rainfall_harvest", "target_net_profit_per_ton"
            ]
            # Only include columns that exist
            display_cols = [col for col in display_cols if col in df_table.columns]
            df_display = df_table[display_cols].head(10)

            self.sugar_data = df_display.to_dict(orient="records")
            
            # Prepare chart data with dates
            chart_cols = ["date", "sugar_price", "ethanol_price", "bagasse_value", 
                         "molasses_value", "ccs_quality", "target_net_profit_per_ton"]
            chart_cols = [col for col in chart_cols if col in df_chart.columns]
            df_chart_display = df_chart[chart_cols].copy()
            
            # Format dates for JSON serialization
            if "date" in df_chart_display.columns:
                df_chart_display["date"] = df_chart_display["date"].dt.strftime("%Y-%m-%d")
            
            self.sugar_chart_data = df_chart_display.to_dict(orient="records")
            self.sugar_data_loaded = True
        except Exception as e:
            print("Error loading sugar data:", e)
            self.sugar_data = []
            self.sugar_chart_data = []
            self.sugar_data_loaded = False

    def load_ethanol_data(self) -> None:
        """Load synthetic ethanol dataset for display."""
        try:
            from .model import SugarcaneModel

            model = SugarcaneModel()
            # Generate table data (small sample for table)
            df_table = model.generate_synthetic_data_etanol(num_samples=10)
            
            # Generate chart data (larger sample for charts)
            df_chart = model.generate_synthetic_data_etanol(num_samples=100)

            # Convert to list of dicts and limit columns for display
            display_cols = [
                "ethanol_price", "crude_oil_price", "gasoline_price",
                "ccs_quality", "fermentation_efficiency", "target_ethanol_profit_per_liter"
            ]
            # Only include columns that exist
            display_cols = [col for col in display_cols if col in df_table.columns]
            df_display = df_table[display_cols].head(10)

            self.ethanol_data = df_display.to_dict(orient="records")
            
            # Prepare chart data with dates
            chart_cols = ["date", "ethanol_price", "crude_oil_price", "gasoline_price", 
                         "ccs_quality", "fermentation_efficiency", "target_ethanol_profit_per_liter"]
            chart_cols = [col for col in chart_cols if col in df_chart.columns]
            df_chart_display = df_chart[chart_cols].copy()
            
            # Format dates for JSON serialization
            if "date" in df_chart_display.columns:
                df_chart_display["date"] = df_chart_display["date"].dt.strftime("%Y-%m-%d")
            
            self.ethanol_chart_data = df_chart_display.to_dict(orient="records")
            self.ethanol_data_loaded = True
        except Exception as e:
            print("Error loading ethanol data:", e)
            self.ethanol_data = []
            self.ethanol_chart_data = []
            self.ethanol_data_loaded = False
