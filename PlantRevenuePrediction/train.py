"""Training script for Sugar Profit Prediction Model.

This script trains a Linear Regression model to predict sugar profit per ton
based on various input features like prices, weather conditions, and quality metrics.
"""

from PlantRevenuePrediction.model import SugarcaneModel


def main():
    """Main training function called by the UI or command line."""
    print("\n🌾 Starting Sugar Profit Prediction Model Training 🌾\n")
    
    try:
        # Initialize model with default path for linear regression
        model = SugarcaneModel(model_path="models/sugar_linear_regression.joblib")
        
        # Train the linear regression model
        metrics = model.train_linear_regression(num_samples=5000)
        
        print("\n" + "=" * 60)
        print("✓ Training completed successfully!")
        print(f"✓ Model type: {metrics['model_type']}")
        print(f"✓ Test R² Score: {metrics['r2_test']:.4f}")
        print(f"✓ Test RMSE: {metrics['rmse_test']:.2f}")
        print("=" * 60 + "\n")
        
        return metrics
        
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ Training failed with error:")
        print(f"   {str(e)}")
        print("=" * 60 + "\n")
        raise


if __name__ == "__main__":
    main()
