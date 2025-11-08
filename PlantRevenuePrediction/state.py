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

            train_main()
            self.training_status = "completed"
        except Exception as e:
            self.training_status = "failed"
            print("Training error:", e)

    def start_training(self) -> None:
        """Kick off training in a background thread to avoid blocking request handling."""
        thread = threading.Thread(target=self._run_training_thread, daemon=True)
        thread.start()
        self.training_status = "started"
