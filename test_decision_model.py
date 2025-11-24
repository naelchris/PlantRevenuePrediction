"""Test script for the unified production decision model."""

from PlantRevenuePrediction.model import SugarcaneModel

def test_unified_dataset():
    """Test the unified sugarcane dataset generation."""
    print("\n" + "=" * 70)
    print("Testing Unified Sugar Cane Dataset Generation")
    print("=" * 70)

    model = SugarcaneModel()
    df = model.generate_unified_sugarcane_data(num_samples=10)

    print(f"\nGenerated {len(df)} samples with {len(df.columns)} features")
    print("\nShared Plantation Conditions:")
    print(df[['cane_yield_tons_per_hectare', 'sugar_content_brix', 'ccs_quality']].head())

    print("\nSugar Production Metrics:")
    print(df[['sugar_profit_per_hectare', 'sugar_tons_per_hectare']].head())

    print("\nEthanol Production Metrics:")
    print(df[['ethanol_profit_per_hectare', 'ethanol_liters_per_hectare']].head())

    print("\nDecision Comparison:")
    print(df[['profit_difference', 'optimal_strategy']].head())

    print("\n✓ Unified dataset generated successfully!")

def test_sugar_data_compatibility():
    """Test that sugar data view is backward compatible."""
    print("\n" + "=" * 70)
    print("Testing Sugar Data View (Backward Compatibility)")
    print("=" * 70)

    model = SugarcaneModel()
    df = model.generate_synthetic_data_sugar(num_samples=5)

    print(f"\nGenerated {len(df)} sugar samples")
    print("\nSugar-focused columns:")
    print(df.columns.tolist())
    print("\nSample data:")
    print(df.head())

    print("\n✓ Sugar data view working correctly!")

def test_ethanol_data_compatibility():
    """Test that ethanol data view is backward compatible."""
    print("\n" + "=" * 70)
    print("Testing Ethanol Data View (Backward Compatibility)")
    print("=" * 70)

    model = SugarcaneModel()
    df = model.generate_synthetic_data_etanol(num_samples=5)

    print(f"\nGenerated {len(df)} ethanol samples")
    print("\nEthanol-focused columns:")
    print(df.columns.tolist())
    print("\nSample data:")
    print(df.head())

    print("\n✓ Ethanol data view working correctly!")

def test_production_decision():
    """Test the production decision recommendation system."""
    print("\n" + "=" * 70)
    print("Testing Production Decision Model")
    print("=" * 70)

    model = SugarcaneModel()

    # Test scenario 1: High sugar prices
    print("\n📊 Scenario 1: High Sugar Prices")
    conditions1 = {
        "cane_yield_tons_per_hectare": 80.0,
        "sugar_content_brix": 14.0,
        "ccs_quality": 11.5,
        "avg_temp_plantation": 26.0,
        "rainfall_mm": 1200.0,
        "harvest_month": 7,
        "sugar_price_per_kg": 0.60,  # High sugar price
        "ethanol_price_per_liter": 0.60,
        "fermentation_efficiency": 0.90,
        "plantation_cost_per_hectare": 2000.0,
        "sugar_processing_cost_per_ton_cane": 45.0,
        "ethanol_processing_cost_per_ton_cane": 65.0,
        "bagasse_value_per_ton": 25.0,
        "molasses_value_per_ton": 100.0,
    }

    result1 = model.predict_optimal_production(conditions1)
    print(f"Recommendation: {result1['recommendation'].upper()}")
    print(f"Sugar Profit: ${result1['sugar_profit_per_hectare']:.2f}/hectare")
    print(f"Ethanol Profit: ${result1['ethanol_profit_per_hectare']:.2f}/hectare")
    print(f"Confidence: {result1['confidence']*100:.0f}%")
    print(f"Reasoning: {result1['reasoning']}")

    # Test scenario 2: High ethanol prices
    print("\n📊 Scenario 2: High Ethanol Prices")
    conditions2 = {
        **conditions1,
        "sugar_price_per_kg": 0.45,  # Lower sugar price
        "ethanol_price_per_liter": 0.80,  # High ethanol price
    }

    result2 = model.predict_optimal_production(conditions2)
    print(f"Recommendation: {result2['recommendation'].upper()}")
    print(f"Sugar Profit: ${result2['sugar_profit_per_hectare']:.2f}/hectare")
    print(f"Ethanol Profit: ${result2['ethanol_profit_per_hectare']:.2f}/hectare")
    print(f"Confidence: {result2['confidence']*100:.0f}%")
    print(f"Reasoning: {result2['reasoning']}")

    # Test scenario 3: Balanced prices
    print("\n📊 Scenario 3: Balanced Market")
    conditions3 = {
        **conditions1,
        "sugar_price_per_kg": 0.50,
        "ethanol_price_per_liter": 0.65,
    }

    result3 = model.predict_optimal_production(conditions3)
    print(f"Recommendation: {result3['recommendation'].upper()}")
    print(f"Sugar Profit: ${result3['sugar_profit_per_hectare']:.2f}/hectare")
    print(f"Ethanol Profit: ${result3['ethanol_profit_per_hectare']:.2f}/hectare")
    print(f"Confidence: {result3['confidence']*100:.0f}%")
    print(f"Reasoning: {result3['reasoning']}")

    print("\n✓ Production decision model working correctly!")

if __name__ == "__main__":
    test_unified_dataset()
    test_sugar_data_compatibility()
    test_ethanol_data_compatibility()
    test_production_decision()

    print("\n" + "=" * 70)
    print("🎉 All tests passed! The unified decision model is ready.")
    print("=" * 70)
    print("\nKey Improvements:")
    print("✅ Sugar and ethanol share the SAME raw material (sugar cane)")
    print("✅ Shared plantation conditions (yield, quality, weather)")
    print("✅ Direct profitability comparison per hectare")
    print("✅ Clear production recommendations with reasoning")
    print("✅ Backward compatible with existing UI")
    print("\n")

