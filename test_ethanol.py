#!/usr/bin/env python3
"""Test script to validate ethanol profit prediction implementation."""

import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PlantRevenuePrediction.model import SugarcaneModel

def test_ethanol_implementation():
    """Test the ethanol profit prediction implementation."""
    print("Testing Ethanol Profit Prediction Implementation")
    print("=" * 50)

    # Initialize the model
    ethanol_model_path = "models/ethanol_linear_regression.joblib"
    model = SugarcaneModel(model_path=ethanol_model_path)

    # Test synthetic data generation
    print("\n1. Testing synthetic ethanol data generation...")
    try:
        df = model.generate_synthetic_data_etanol(num_samples=10)
        print(f"✅ Generated {len(df)} samples")
        print("Columns:", list(df.columns))
        print("\nFirst few rows:")
        print(df.head())
    except Exception as e:
        print(f"❌ Data generation failed: {e}")
        return False

    # Test training
    print("\n2. Testing ethanol model training...")
    try:
        metrics = model.train_linear_regression_ethanol(num_samples=100)
        print(f"✅ Training successful!")
        print(f"R² Score: {metrics['r2_test']:.4f}")
        print(f"RMSE: {metrics['rmse_test']:.4f}")
    except Exception as e:
        print(f"❌ Training failed: {e}")
        return False

    # Test prediction
    print("\n3. Testing ethanol profit prediction...")
    try:
        test_scenario = {
            "ethanol_price": 0.55,
            "crude_oil_price": 80.0,
            "gasoline_price": 2.5,
            "ccs_quality": 11.5,
            "fermentation_efficiency": 0.92,
            "harvest_month": 6
        }

        prediction = model.predict_ethanol(test_scenario)
        print(f"✅ Prediction successful!")
        print(f"Input scenario: {test_scenario}")
        print(f"Predicted ethanol profit per liter: ${prediction:.4f}")
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        return False

    print("\n✅ All ethanol implementation tests passed!")
    return True

if __name__ == "__main__":
    success = test_ethanol_implementation()
    sys.exit(0 if success else 1)
