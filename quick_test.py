# ...new file...
from PlantRevenuePrediction.model import SugarcaneModel


def smoke_test():
    m = SugarcaneModel()
    stats = m.train(num_samples=200, n_estimators=10, max_depth=5)
    print("Train stats:", stats)
    scenario = {
        "sugar_price": 800.0,
        "ethanol_price": 0.45,
        "bagasse_value": 25.0,
        "molasses_value": 8.0,
        "avg_temp_plantation": 26.0,
        "rainfall_harvest": 120.0,
        "ccs_quality": 12.0,
        "harvest_month": 9,
    }
    pred = m.predict(scenario)
    print("Predicted profit per ton:", pred)


if __name__ == "__main__":
    smoke_test()

