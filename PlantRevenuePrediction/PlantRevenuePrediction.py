"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from .state import State


def slider_input(label: str, value, min_val: float, max_val: float, step: float, on_change, unit: str = "") -> rx.Component:
    """Helper function to create a modern slider with label and value display."""
    return rx.box(
        rx.vstack(
            # Label and current value display
            rx.hstack(
                rx.text(label, weight="medium", size="3"),
                rx.spacer(),
                rx.badge(
                    f"{value}{unit}",
                    radius="full",
                    size="2",
                    variant="soft",
                    color_scheme="grass",
                ),
                width="100%",
                align="center",
            ),
            # Slider
            rx.slider(
                value=[value],
                min=min_val,
                max=max_val,
                step=step,
                on_change=lambda val: on_change(val[0]),
                color_scheme="grass",
                size="2",
                width="100%",
                cursor="pointer",
            ),
            spacing="2",
            width="100%",
        ),
        padding="3",
        border_radius="lg",
        border="1px solid var(--gray-a5)",
        background="var(--gray-a2)",
        width="100%",
        _hover={
            "border_color": "var(--grass-a7)",
            "background": "var(--gray-a3)",
        },
        transition="all 0.2s ease",
    )


def line_chart(title: str, data, x_key: str, y_keys: list[str], colors: list[str]) -> rx.Component:
    """Create a line chart component for time-series data visualization."""
    return rx.box(
        rx.vstack(
            rx.heading(title, size="5", margin_bottom="3"),
            rx.recharts.line_chart(
                *[
                    rx.recharts.line(
                        data_key=y_key,
                        stroke=color,
                        type_="monotone",
                        stroke_width=2,
                    )
                    for y_key, color in zip(y_keys, colors)
                ],
                rx.recharts.x_axis(
                    data_key=x_key,
                    tick={"fill": "var(--gray-11)", "fontSize": 12},
                    stroke="var(--gray-7)",
                ),
                rx.recharts.y_axis(
                    tick={"fill": "var(--gray-11)", "fontSize": 12},
                    stroke="var(--gray-7)",
                ),
                rx.recharts.cartesian_grid(
                    stroke_dasharray="3 3",
                    stroke="var(--gray-5)",
                ),
                rx.recharts.legend(),
                rx.recharts.tooltip(
                    content_style={
                        "backgroundColor": "var(--gray-1)",
                        "border": "1px solid var(--gray-7)",
                        "borderRadius": "8px",
                    },
                ),
                data=data,
                width="100%",
                height=300,
            ),
            spacing="2",
            width="100%",
        ),
        padding="4",
        border="1px solid var(--gray-a5)",
        border_radius="lg",
        background="var(--gray-a2)",
        width="100%",
    )


def decision_dashboard() -> rx.Component:
    """Decision dashboard showing sugar vs ethanol production comparison."""
    return rx.box(
        rx.vstack(
            rx.heading("🌱 Production Decision Dashboard", size="7", margin_bottom="3"),
            rx.text(
                "Compare profitability of sugar vs ethanol production from the same sugar cane",
                size="3",
                color="gray",
                margin_bottom="4",
            ),

            # Shared Plantation Conditions
            rx.box(
                rx.vstack(
                    rx.heading("🌾 Shared Plantation Conditions", size="5", margin_bottom="3"),
                    rx.text("These conditions are the same for both sugar and ethanol production",
                           size="2", color="gray", margin_bottom="2"),

                    rx.grid(
                        slider_input(
                            "Cane Yield",
                            State.cane_yield_tons_per_hectare,
                            40.0, 120.0, 1.0,
                            State.set_cane_yield,
                            " tons/hectare"
                        ),
                        slider_input(
                            "Sugar Content (Brix)",
                            State.sugar_content_brix,
                            10.0, 18.0, 0.1,
                            State.set_sugar_content_brix,
                            " %"
                        ),
                        slider_input(
                            "CCS Quality",
                            State.ccs_quality,
                            9.0, 14.0, 0.1,
                            State.set_ccs_quality,
                            " %"
                        ),
                        slider_input(
                            "Temperature",
                            State.avg_temp_plantation,
                            20.0, 32.0, 0.5,
                            State.set_avg_temp_plantation,
                            " °C"
                        ),
                        slider_input(
                            "Rainfall",
                            State.rainfall_mm,
                            600.0, 2000.0, 50.0,
                            State.set_rainfall_mm,
                            " mm"
                        ),
                        slider_input(
                            "Harvest Month",
                            State.harvest_month,
                            1, 12, 1,
                            State.set_harvest_month,
                            ""
                        ),
                        columns="2",
                        spacing="3",
                        width="100%",
                    ),
                    spacing="2",
                    width="100%",
                ),
                padding="4",
                border="2px solid var(--grass-7)",
                border_radius="lg",
                background="var(--grass-2)",
                width="100%",
                margin_bottom="4",
            ),

            # Market Prices and Costs
            rx.grid(
                # Sugar column
                rx.box(
                    rx.vstack(
                        rx.heading("🍯 Sugar Production", size="5"),
                        slider_input("Sugar Price", State.sugar_price, 400.0, 800.0, 10.0,
                                    State.set_sugar_price, " $/ton"),
                        slider_input("Processing Cost", State.sugar_processing_cost, 30.0, 70.0, 1.0,
                                    State.set_sugar_processing_cost, " $/ton cane"),
                        slider_input("Bagasse Value", State.bagasse_value, 10.0, 40.0, 1.0,
                                    State.set_bagasse_value, " $/ton"),
                        slider_input("Molasses Value", State.molasses_value, 50.0, 200.0, 5.0,
                                    State.set_molasses_value, " $/ton"),
                        spacing="3",
                        width="100%",
                    ),
                    padding="4",
                    border="1px solid var(--orange-7)",
                    border_radius="lg",
                    background="var(--orange-2)",
                ),

                # Ethanol column
                rx.box(
                    rx.vstack(
                        rx.heading("⚗️ Ethanol Production", size="5"),
                        slider_input("Ethanol Price", State.ethanol_price, 0.3, 1.0, 0.01,
                                    State.set_ethanol_price, " $/L"),
                        slider_input("Processing Cost", State.ethanol_processing_cost, 50.0, 90.0, 1.0,
                                    State.set_ethanol_processing_cost, " $/ton cane"),
                        slider_input("Fermentation Efficiency", State.fermentation_efficiency,
                                    0.85, 0.98, 0.01, State.set_fermentation_efficiency, ""),
                        slider_input("Crude Oil Price", State.crude_oil_price, 50.0, 120.0, 1.0,
                                    State.set_crude_oil_price, " $/barrel"),
                        spacing="3",
                        width="100%",
                    ),
                    padding="4",
                    border="1px solid var(--blue-7)",
                    border_radius="lg",
                    background="var(--blue-2)",
                ),

                columns="2",
                spacing="4",
                width="100%",
                margin_bottom="4",
            ),

            # Calculate Button
            rx.button(
                "🧮 Calculate Optimal Strategy",
                on_click=State.predict_optimal_strategy,
                size="4",
                color_scheme="purple",
                width="100%",
                margin_bottom="4",
            ),

            # Results Display
            rx.cond(
                State.show_decision_results,
                rx.vstack(
                    # Comparison Cards
                    rx.hstack(
                        # Sugar card
                        rx.box(
                            rx.vstack(
                                rx.text("🍯 Sugar Production", weight="bold", size="4"),
                                rx.heading(f"${State.sugar_profit_per_hectare:.0f}", size="8", color="orange"),
                                rx.text("per hectare", size="2", color="gray"),
                                rx.divider(),
                                rx.text(f"Yields: {State.sugar_production_tons:.1f} tons sugar", size="2"),
                                spacing="2",
                                align="center",
                            ),
                            padding="4",
                            border="2px solid var(--orange-7)",
                            border_radius="lg",
                            background="var(--orange-3)",
                            flex="1",
                        ),

                        # VS indicator
                        rx.box(
                            rx.vstack(
                                rx.text("VS", size="8", weight="bold"),
                                rx.text(f"Δ ${abs(State.profit_difference):.0f}", size="2"),
                                spacing="1",
                                align="center",
                            ),
                            padding="2",
                        ),

                        # Ethanol card
                        rx.box(
                            rx.vstack(
                                rx.text("⚗️ Ethanol Production", weight="bold", size="4"),
                                rx.heading(f"${State.ethanol_profit_per_hectare:.0f}", size="8", color="blue"),
                                rx.text("per hectare", size="2", color="gray"),
                                rx.divider(),
                                rx.text(f"Yields: {State.ethanol_production_liters:.0f} liters ethanol", size="2"),
                                spacing="2",
                                align="center",
                            ),
                            padding="4",
                            border="2px solid var(--blue-7)",
                            border_radius="lg",
                            background="var(--blue-3)",
                            flex="1",
                        ),

                        spacing="4",
                        width="100%",
                        align="center",
                    ),

                    # Recommendation Box
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.text("📋 Recommendation:", weight="bold", size="5"),
                                rx.badge(
                                    State.production_recommendation.upper(),
                                    size="3",
                                    variant="solid",
                                    color_scheme=rx.cond(
                                        State.production_recommendation == "sugar",
                                        "orange",
                                        rx.cond(
                                            State.production_recommendation == "ethanol",
                                            "blue",
                                            "purple"
                                        )
                                    ),
                                ),
                                spacing="3",
                                align="center",
                            ),
                            rx.text(State.recommendation_reasoning, size="3"),
                            rx.divider(),
                            rx.hstack(
                                rx.text(f"Confidence: {State.recommendation_confidence * 100:.0f}%", size="2", weight="medium"),
                                rx.progress(value=(State.recommendation_confidence * 100).to(int), size="2", color_scheme="purple"),
                                spacing="2",
                                width="100%",
                                align="center",
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        padding="4",
                        border="2px solid var(--purple-7)",
                        border_radius="lg",
                        background="var(--purple-2)",
                        width="100%",
                    ),

                    spacing="4",
                    width="100%",
                ),
            ),

            spacing="4",
            width="100%",
        ),
        padding="6",
        width="100%",
    )


def data_table(title: str, data, load_action, is_sugar: bool) -> rx.Component:
    """Helper function to create a styled data table similar to the task list."""
    is_loaded = State.sugar_data_loaded if is_sugar else State.ethanol_data_loaded

    # Define columns based on table type
    if is_sugar:
        columns = ["sugar_price", "ethanol_price", "ccs_quality", "avg_temp_plantation", "rainfall_harvest", "target_net_profit_per_ton"]
    else:
        columns = [
            "date", "ethanol_price", "crude_oil_price", "gasoline_price",
            "ccs_quality", "fermentation_efficiency", "harvest_month",
            "cane_yield_tons_per_hectare", "sugar_content_brix",
            "avg_temp_plantation", "rainfall_harvest",
            "ethanol_profit_per_hectare", "target_ethanol_profit_per_1000_liter",
        ]

    # Min width per cell so all columns stay readable
    cell_min_w = "130px"

    def render_table():
        """Render the table with headers and rows.

        One container handles BOTH horizontal and vertical scroll so the
        header row scrolls in sync with the data when the user pans left/right,
        while still sticking to the top on vertical scroll.
        """
        return rx.box(
            # Single container — both axes scroll together
            rx.box(
                # Header (sticky-top inside the shared scroll container)
                rx.hstack(
                    *[
                        rx.box(
                            rx.text(col.replace("_", " ").title(), weight="bold", size="2"),
                            min_width=cell_min_w,
                            padding="2",
                        )
                        for col in columns
                    ],
                    width="max-content",
                    min_width="100%",
                    background_color="#f0f0f0",
                    border_bottom="1px solid #e2e8f0",
                    position="sticky",
                    top="0",
                    z_index="1",
                ),
                # Data rows
                rx.vstack(
                    rx.foreach(
                        data,
                        lambda row: rx.hstack(
                            *[
                                rx.box(
                                    rx.text(row[col], size="2"),
                                    min_width=cell_min_w,
                                    padding="2",
                                )
                                for col in columns
                            ],
                            width="max-content",
                            min_width="100%",
                            border_bottom="1px solid #e2e8f0",
                        )
                    ),
                    spacing="0",
                    width="max-content",
                    min_width="100%",
                ),
                # Single scroll container: horizontal + vertical
                overflow_x="auto",
                overflow_y="auto",
                max_height="500px",
                width="100%",
            ),
            width="100%",
            border="1px solid #e2e8f0",
            border_radius="md",
        )

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading(title, size="6"),
                rx.button("Load Data", on_click=load_action),
                width="100%",
                justify="between",
            ),
            rx.cond(
                is_loaded,
                render_table(),
                rx.text("No data loaded. Click 'Load Data' to generate sample dataset.", color="gray"),
            ),
            spacing="4",
            width="100%",
        ),
        padding="4",
        border="1px solid #e2e8f0",
        border_radius="md",
        width="100%",
    )


def index() -> rx.Component:
    # Welcome Page (Index) with split layout
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            # Header with navigation
            rx.hstack(
                rx.heading("Sugar Cane Plant Revenue Prediction 👋", size="9"),
                rx.spacer(),
                rx.hstack(
                    rx.link(
                        rx.button("📊 Predictions", variant="solid", color_scheme="green", size="3"),
                        href="/",
                    ),
                    rx.link(
                        rx.button("🌱 Decision Dashboard", variant="soft", size="3"),
                        href="/decision",
                    ),
                    rx.link(
                        rx.button("📚 Documentation", variant="soft", size="3"),
                        href="/explanation",
                    ),
                    spacing="3",
                ),
                width="100%",
                align="center",
                margin_bottom="4",
            ),

            # Main Split Layout: Sugar (Left) | Ethanol (Right)
            rx.grid(
                # ========== LEFT SIDE: SUGAR PROFIT PREDICTION ==========
                rx.box(
                    rx.vstack(
                        rx.heading("🌾 Sugar Production", size="7", color="green"),
                        
                        # Sugar Data Table
                        data_table("Sugar Dataset", State.sugar_data, State.load_sugar_data, True),
                        
                        # Sugar Charts
                        rx.cond(
                            State.sugar_data_loaded,
                            rx.vstack(
                                rx.heading("Sugar Data Trends", size="6", margin_top="3"),
                                line_chart(
                                    "Sugar Price Over Time",
                                    State.sugar_chart_data,
                                    "date",
                                    ["sugar_price"],
                                    ["#10b981"]
                                ),
                                line_chart(
                                    "Ethanol Price Over Time",
                                    State.sugar_chart_data,
                                    "date",
                                    ["ethanol_price"],
                                    ["#3b82f6"]
                                ),
                                line_chart(
                                    "Byproduct Values",
                                    State.sugar_chart_data,
                                    "date",
                                    ["bagasse_value", "molasses_value"],
                                    ["#f59e0b", "#8b5cf6"]
                                ),
                                line_chart(
                                    "Quality & Profit",
                                    State.sugar_chart_data,
                                    "date",
                                    ["ccs_quality", "target_net_profit_per_ton"],
                                    ["#ef4444", "#06b6d4"]
                                ),
                                spacing="3",
                                width="100%",
                            ),
                        ),
                        
                        # Sugar Input Parameters
                        rx.vstack(
                            rx.heading("Sugar Parameters", size="5", margin_top="4"),
                            slider_input(
                                "Sugar Price",
                                State.sugar_price,
                                min_val=500.0,
                                max_val=1000.0,
                                step=10.0,
                                on_change=State.set_sugar_price,
                                unit=" $/ton"
                            ),
                            slider_input(
                                "Bagasse Value",
                                State.bagasse_value,
                                min_val=10.0,
                                max_val=40.0,
                                step=1.0,
                                on_change=State.set_bagasse_value,
                                unit=" $/ton"
                            ),
                            slider_input(
                                "Molasses Value",
                                State.molasses_value,
                                min_val=5.0,
                                max_val=15.0,
                                step=0.5,
                                on_change=State.set_molasses_value,
                                unit=" $/ton"
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        
                        # Common Parameters for Sugar
                        rx.vstack(
                            rx.heading("Environment & Quality", size="5", margin_top="3"),
                            slider_input(
                                "Plantation Temperature",
                                State.avg_temp_plantation,
                                min_val=20.0,
                                max_val=32.0,
                                step=0.5,
                                on_change=State.set_avg_temp_plantation,
                                unit=" °C"
                            ),
                            slider_input(
                                "Rainfall at Harvest",
                                State.rainfall_harvest,
                                min_val=50.0,
                                max_val=300.0,
                                step=5.0,
                                on_change=State.set_rainfall_harvest,
                                unit=" mm"
                            ),
                            slider_input(
                                "CCS Quality",
                                State.ccs_quality,
                                min_val=9.0,
                                max_val=14.0,
                                step=0.1,
                                on_change=State.set_ccs_quality,
                                unit=" %"
                            ),
                            slider_input(
                                "Harvest Month",
                                State.harvest_month,
                                min_val=1,
                                max_val=12,
                                step=1,
                                on_change=State.set_harvest_month,
                                unit=""
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        
                        # Sugar Prediction Button & Result
                        rx.vstack(
                            rx.button(
                                "Predict Sugar Profit",
                                on_click=State.predict_profit,
                                size="3",
                                color_scheme="green",
                                width="100%",
                            ),
                            rx.button(
                                "Train Model",
                                on_click=State.start_training,
                                size="2",
                                variant="soft",
                                width="100%",
                                loading=State.training_status == "running",
                            ),
                            
                            # Training Results Display
                            rx.cond(
                                State.show_training_results,
                                rx.box(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.text("📊 Training Results", weight="bold", size="3"),
                                            rx.badge(
                                                "Completed",
                                                color_scheme="green",
                                                variant="soft",
                                            ),
                                            width="100%",
                                            justify="between",
                                            align="center",
                                        ),
                                        rx.grid(
                                            rx.box(
                                                rx.text("R² Score", size="1", color="gray"),
                                                rx.text(
                                                    f"{State.training_metrics.get('r2_test', 0):.4f}",
                                                    size="4",
                                                    weight="bold",
                                                    color="green",
                                                ),
                                                padding="2",
                                                text_align="center",
                                            ),
                                            rx.box(
                                                rx.text("RMSE", size="1", color="gray"),
                                                rx.text(
                                                    f"{State.training_metrics.get('rmse_test', 0):.2f}",
                                                    size="4",
                                                    weight="bold",
                                                    color="blue",
                                                ),
                                                padding="2",
                                                text_align="center",
                                            ),
                                            rx.box(
                                                rx.text("MAE", size="1", color="gray"),
                                                rx.text(
                                                    f"{State.training_metrics.get('mae_test', 0):.2f}",
                                                    size="4",
                                                    weight="bold",
                                                    color="purple",
                                                ),
                                                padding="2",
                                                text_align="center",
                                            ),
                                            columns="3",
                                            spacing="2",
                                            width="100%",
                                        ),
                                        rx.text(
                                            f"Trained on {State.training_metrics.get('n_train', 0)} samples",
                                            size="1",
                                            color="gray",
                                        ),
                                        spacing="2",
                                        width="100%",
                                    ),
                                    padding="3",
                                    border="1px solid var(--green-6)",
                                    border_radius="md",
                                    background="var(--green-1)",
                                    width="100%",
                                ),
                            ),
                            
                            # Training Status Indicator
                            rx.cond(
                                State.training_status == "running",
                                rx.box(
                                    rx.hstack(
                                        rx.spinner(size="2"),
                                        rx.text("Training in progress...", size="2"),
                                        spacing="2",
                                        align="center",
                                    ),
                                    padding="2",
                                    border_radius="md",
                                    background="var(--blue-2)",
                                    width="100%",
                                ),
                            ),
                            
                            rx.box(
                                rx.text("Predicted Net Profit Per Ton:", size="2", weight="medium"),
                                rx.heading(f"${State.predicted_profit:.2f}", size="8", color="green"),
                                padding="4",
                                border="2px solid var(--green-7)",
                                border_radius="lg",
                                background="var(--green-2)",
                                text_align="center",
                                width="100%",
                            ),
                            spacing="3",
                            width="100%",
                            margin_top="4",
                        ),
                        
                        spacing="4",
                        width="100%",
                    ),
                    padding="6",
                    padding_right="8",
                    border_right="2px solid var(--gray-5)",
                ),
                
                # ========== RIGHT SIDE: ETHANOL PROFIT PREDICTION ==========
                rx.box(
                    rx.vstack(
                        rx.heading("⚗️ Ethanol Production", size="7", color="blue"),
                        
                        # Ethanol Data Table
                        data_table("Ethanol Dataset", State.ethanol_data, State.load_ethanol_data, False),
                        
                        # Ethanol Charts
                        rx.cond(
                            State.ethanol_data_loaded,
                            rx.vstack(
                                rx.heading("Ethanol Data Trends", size="6", margin_top="3"),
                                line_chart(
                                    "Market Prices",
                                    State.ethanol_chart_data,
                                    "date",
                                    ["ethanol_price", "crude_oil_price", "gasoline_price"],
                                    ["#10b981", "#f59e0b", "#ef4444"]
                                ),
                                line_chart(
                                    "Production Metrics",
                                    State.ethanol_chart_data,
                                    "date",
                                    ["ccs_quality", "fermentation_efficiency"],
                                    ["#8b5cf6", "#06b6d4"]
                                ),
                                line_chart(
                                    "Profit Per 1000 Liters",
                                    State.ethanol_chart_data,
                                    "date",
                                    ["target_ethanol_profit_per_1000_liter"],
                                    ["#3b82f6"]
                                ),
                                spacing="3",
                                width="100%",
                            ),
                        ),
                        
                        # Ethanol Input Parameters
                        rx.vstack(
                            rx.heading("Ethanol Parameters", size="5", margin_top="4"),
                            slider_input(
                                "Ethanol Price",
                                State.ethanol_price,
                                min_val=0.3,
                                max_val=1.0,
                                step=0.01,
                                on_change=State.set_ethanol_price,
                                unit=" $/L"
                            ),
                            slider_input(
                                "Crude Oil Price",
                                State.crude_oil_price,
                                min_val=50.0,
                                max_val=120.0,
                                step=1.0,
                                on_change=State.set_crude_oil_price,
                                unit=" $/barrel"
                            ),
                            slider_input(
                                "Gasoline Price",
                                State.gasoline_price,
                                min_val=1.50,
                                max_val=3.50,
                                step=0.05,
                                on_change=State.set_gasoline_price,
                                unit=" $/gal"
                            ),
                            slider_input(
                                "Fermentation Efficiency",
                                State.fermentation_efficiency,
                                min_val=0.85,
                                max_val=0.98,
                                step=0.01,
                                on_change=State.set_fermentation_efficiency,
                                unit=""
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        
                        # Common Parameters for Ethanol (CCS Quality and Harvest Month)
                        rx.vstack(
                            rx.heading("Production Quality", size="5", margin_top="3"),
                            slider_input(
                                "CCS Quality",
                                State.ccs_quality,
                                min_val=9.0,
                                max_val=14.0,
                                step=0.1,
                                on_change=State.set_ccs_quality,
                                unit=" %"
                            ),
                            slider_input(
                                "Harvest Month",
                                State.harvest_month,
                                min_val=1,
                                max_val=12,
                                step=1,
                                on_change=State.set_harvest_month,
                                unit=""
                            ),
                            spacing="3",
                            width="100%",
                        ),

                        # Ethanol Prediction Button & Result
                        rx.vstack(
                            rx.button(
                                "Predict Ethanol Profit",
                                on_click=State.predict_ethanol_profit,
                                size="3",
                                color_scheme="blue",
                                width="100%",
                            ),
                            rx.button(
                                "Train Ethanol Model",
                                on_click=State.start_ethanol_training,
                                size="2",
                                variant="soft",
                                width="100%",
                                loading=State.ethanol_training_status == "running",
                            ),

                            # Ethanol Training Results Display
                            rx.cond(
                                State.show_ethanol_training_results,
                                rx.box(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.text("📊 Ethanol Training Results", weight="bold", size="3"),
                                            rx.badge(
                                                "Completed",
                                                color_scheme="blue",
                                                variant="soft",
                                            ),
                                            width="100%",
                                            justify="between",
                                            align="center",
                                        ),
                                        rx.grid(
                                            rx.box(
                                                rx.text("R² Score", size="1", color="gray"),
                                                rx.text(
                                                    f"{State.ethanol_training_metrics.get('r2_test', 0):.4f}",
                                                    size="4",
                                                    weight="bold",
                                                    color="blue",
                                                ),
                                                padding="2",
                                                text_align="center",
                                            ),
                                            rx.box(
                                                rx.text("RMSE", size="1", color="gray"),
                                                rx.text(
                                                    f"{State.ethanol_training_metrics.get('rmse_test', 0):.2f}",
                                                    size="4",
                                                    weight="bold",
                                                    color="green",
                                                ),
                                                padding="2",
                                                text_align="center",
                                            ),
                                            rx.box(
                                                rx.text("MAE", size="1", color="gray"),
                                                rx.text(
                                                    f"{State.ethanol_training_metrics.get('mae_test', 0):.2f}",
                                                    size="4",
                                                    weight="bold",
                                                    color="purple",
                                                ),
                                                padding="2",
                                                text_align="center",
                                            ),
                                            columns="3",
                                            spacing="2",
                                            width="100%",
                                        ),
                                        rx.text(
                                            f"Trained on {State.ethanol_training_metrics.get('n_train', 0)} samples",
                                            size="1",
                                            color="gray",
                                        ),
                                        spacing="2",
                                        width="100%",
                                    ),
                                    padding="3",
                                    border="1px solid var(--blue-6)",
                                    border_radius="md",
                                    background="var(--blue-1)",
                                    width="100%",
                                ),
                            ),

                            # Ethanol Training Status Indicator
                            rx.cond(
                                State.ethanol_training_status == "running",
                                rx.box(
                                    rx.hstack(
                                        rx.spinner(size="2"),
                                        rx.text("Ethanol training in progress...", size="2"),
                                        spacing="2",
                                        align="center",
                                    ),
                                    padding="2",
                                    border_radius="md",
                                    background="var(--blue-2)",
                                    width="100%",
                                ),
                            ),

                            rx.box(
                                rx.text("Predicted Ethanol Profit Per 1000 Liters:", size="2", weight="medium"),
                                rx.heading(f"${State.predicted_ethanol_profit:.4f}", size="8", color="blue"),
                                padding="4",
                                border="2px solid var(--blue-7)",
                                border_radius="lg",
                                background="var(--blue-2)",
                                text_align="center",
                                width="100%",
                            ),
                            spacing="3",
                            width="100%",
                            margin_top="4",
                        ),
                        
                        spacing="4",
                        width="100%",
                    ),
                    padding="6",
                    padding_left="8",
                ),
                
                columns="2",
                spacing="6",
                width="100%",
            ),
            
            spacing="4",
            width="100%",
            min_height="85vh",
        ),
        size="4",
    )


def decision_page() -> rx.Component:
    """Page for production decision comparison."""
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            # Header with navigation
            rx.hstack(
                rx.heading("Sugar Cane Plant Revenue Prediction 👋", size="9"),
                rx.spacer(),
                rx.hstack(
                    rx.link(
                        rx.button("📊 Predictions", variant="soft", size="3"),
                        href="/",
                    ),
                    rx.link(
                        rx.button("🌱 Decision Dashboard", variant="solid", color_scheme="purple", size="3"),
                        href="/decision",
                    ),
                    rx.link(
                        rx.button("📚 Documentation", variant="soft", size="3"),
                        href="/explanation",
                    ),
                    spacing="3",
                ),
                width="100%",
                align="center",
                margin_bottom="4",
            ),

            # Decision Dashboard
            decision_dashboard(),

            spacing="4",
            width="100%",
            min_height="85vh",
        ),
        size="4",
    )


def explanation_page() -> rx.Component:
    """Page displaying comprehensive documentation."""
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            # Header with navigation
            rx.hstack(
                rx.heading("Sugar Cane Plant Revenue Prediction 👋", size="9"),
                rx.spacer(),
                rx.hstack(
                    rx.link(
                        rx.button("📊 Predictions", variant="soft", size="3"),
                        href="/",
                    ),
                    rx.link(
                        rx.button("🌱 Decision Dashboard", variant="soft", size="3"),
                        href="/decision",
                    ),
                    rx.link(
                        rx.button("📚 Documentation", variant="solid", color_scheme="blue", size="3"),
                        href="/explanation",
                    ),
                    spacing="3",
                ),
                width="100%",
                align="center",
                margin_bottom="4",
            ),

            # Documentation Content
            rx.vstack(
                rx.heading("📚 System Documentation", size="8", margin_bottom="3"),
                rx.text(
                    "Comprehensive guides for the Realistic Sugar Cane Production Decision System",
                    size="4",
                    color="gray",
                    margin_bottom="4",
                ),

                # Quick Start Section
                rx.box(
                    rx.vstack(
                        rx.heading("🚀 Quick Start Guide", size="6", color="green"),
                        rx.divider(margin_y="3"),

                        rx.text("Your Realistic Sugar Cane Decision System is Ready!", weight="bold", size="4"),

                        rx.heading("✅ What You Can Do Now", size="5", margin_top="4"),

                        rx.vstack(
                            rx.text("1. View the Decision Dashboard", weight="bold"),
                            rx.text("   Navigate to the Decision Dashboard tab or visit /decision", color="gray"),
                            rx.text("   Compare sugar vs ethanol production profitability side-by-side", color="gray"),

                            rx.text("2. Run the Tests", weight="bold", margin_top="3"),
                            rx.code("python3 test_decision_model.py", margin_top="2"),
                            rx.text("   Verify everything works correctly", color="gray"),

                            rx.text("3. Try Example Scenarios", weight="bold", margin_top="3"),
                            rx.vstack(
                                rx.text("• High Sugar Prices: Sugar price $600/ton, Ethanol $0.60/L → Should recommend SUGAR", size="2"),
                                rx.text("• High Ethanol Demand: Sugar $450/ton, Ethanol $0.85/L → Test ethanol preference", size="2"),
                                rx.text("• Poor Quality Cane: Low yield 50 tons/ha, 11% Brix → See impact on both", size="2"),
                                spacing="2",
                            ),

                            spacing="3",
                            align="start",
                        ),

                        rx.heading("🎯 The Big Improvement", size="5", margin_top="4"),
                        rx.grid(
                            rx.box(
                                rx.vstack(
                                    rx.text("❌ Before (Unrealistic)", weight="bold", color="red"),
                                    rx.text("• Field A: Sugar Cane", size="2"),
                                    rx.text("• Field B: Sugar Cane", size="2"),
                                    rx.text("• Independent models", size="2"),
                                    rx.text("• No connection!", size="2"),
                                    spacing="2",
                                ),
                                padding="3",
                                border="1px solid var(--red-7)",
                                border_radius="md",
                                background="var(--red-2)",
                            ),
                            rx.box(
                                rx.vstack(
                                    rx.text("✅ After (Realistic)", weight="bold", color="green"),
                                    rx.text("• Same Field: ONE harvest", size="2"),
                                    rx.text("• Choose: Sugar OR Ethanol", size="2"),
                                    rx.text("• Direct comparison", size="2"),
                                    rx.text("• Real decision support!", size="2"),
                                    spacing="2",
                                ),
                                padding="3",
                                border="1px solid var(--green-7)",
                                border_radius="md",
                                background="var(--green-2)",
                            ),
                            columns="2",
                            spacing="4",
                        ),

                        spacing="3",
                        align="start",
                    ),
                    padding="4",
                    border="1px solid var(--green-7)",
                    border_radius="lg",
                    background="var(--green-1)",
                    width="100%",
                    margin_bottom="4",
                ),

                # Key Features Section
                rx.box(
                    rx.vstack(
                        rx.heading("💡 Key Features", size="6", color="blue"),
                        rx.divider(margin_y="3"),

                        rx.grid(
                            rx.box(
                                rx.vstack(
                                    rx.text("🌾 Shared Plantation", weight="bold", size="3"),
                                    rx.text("Same cane yield, sugar content, quality, weather, and growing costs for both products", size="2"),
                                    spacing="2",
                                ),
                                padding="3",
                                border="1px solid var(--blue-5)",
                                border_radius="md",
                            ),
                            rx.box(
                                rx.vstack(
                                    rx.text("📊 Direct Comparison", weight="bold", size="3"),
                                    rx.text("Sugar profit vs Ethanol profit per hectare with opportunity cost analysis", size="2"),
                                    spacing="2",
                                ),
                                padding="3",
                                border="1px solid var(--blue-5)",
                                border_radius="md",
                            ),
                            rx.box(
                                rx.vstack(
                                    rx.text("🧮 Smart Recommendations", weight="bold", size="3"),
                                    rx.text("SUGAR, ETHANOL, or MIXED strategy based on profitability difference", size="2"),
                                    spacing="2",
                                ),
                                padding="3",
                                border="1px solid var(--blue-5)",
                                border_radius="md",
                            ),
                            rx.box(
                                rx.vstack(
                                    rx.text("🎯 Confidence Scoring", weight="bold", size="3"),
                                    rx.text("Visual confidence indicator showing certainty of recommendation", size="2"),
                                    spacing="2",
                                ),
                                padding="3",
                                border="1px solid var(--blue-5)",
                                border_radius="md",
                            ),
                            columns="2",
                            spacing="3",
                        ),

                        spacing="3",
                        align="start",
                    ),
                    padding="4",
                    border="1px solid var(--blue-7)",
                    border_radius="lg",
                    background="var(--blue-1)",
                    width="100%",
                    margin_bottom="4",
                ),

                # Example Scenario Section
                rx.box(
                    rx.vstack(
                        rx.heading("📊 Example Scenario", size="6", color="purple"),
                        rx.divider(margin_y="3"),

                        rx.vstack(
                            rx.text("🌾 Plantation Conditions:", weight="bold"),
                            rx.text("• Yield: 80 tons/hectare", size="2"),
                            rx.text("• Sugar content: 14%", size="2"),
                            rx.text("• Quality: 11.5 CCS", size="2"),
                            rx.text("• Temperature: 26°C", size="2"),
                            spacing="1",
                        ),

                        rx.vstack(
                            rx.text("💰 Market Prices:", weight="bold", margin_top="3"),
                            rx.text("• Sugar: $0.50/kg ($500/ton)", size="2"),
                            rx.text("• Ethanol: $0.65/liter", size="2"),
                            spacing="1",
                        ),

                        rx.box(
                            rx.vstack(
                                rx.text("📈 RESULTS:", weight="bold", size="4"),
                                rx.hstack(
                                    rx.box(
                                        rx.vstack(
                                            rx.text("🍯 Sugar", weight="bold"),
                                            rx.text("$992/hectare", size="5", color="green"),
                                            rx.text("✅ Profitable", size="2"),
                                            spacing="1",
                                        ),
                                        padding="3",
                                        border="1px solid var(--green-7)",
                                        border_radius="md",
                                        background="var(--green-2)",
                                        flex="1",
                                    ),
                                    rx.box(
                                        rx.vstack(
                                            rx.text("⚗️ Ethanol", weight="bold"),
                                            rx.text("-$2,708/hectare", size="5", color="red"),
                                            rx.text("❌ Loss", size="2"),
                                            spacing="1",
                                        ),
                                        padding="3",
                                        border="1px solid var(--red-7)",
                                        border_radius="md",
                                        background="var(--red-2)",
                                        flex="1",
                                    ),
                                    spacing="3",
                                    width="100%",
                                ),
                                rx.box(
                                    rx.vstack(
                                        rx.text("📋 Recommendation: SUGAR", weight="bold", size="4"),
                                        rx.text("💡 Sugar is $3,700 more profitable", size="3"),
                                        rx.text("🎯 Confidence: 100%", size="3"),
                                        spacing="2",
                                    ),
                                    padding="3",
                                    border="2px solid var(--purple-7)",
                                    border_radius="md",
                                    background="var(--purple-2)",
                                    width="100%",
                                    margin_top="3",
                                ),
                                spacing="3",
                            ),
                            padding="3",
                            border="1px solid var(--gray-5)",
                            border_radius="md",
                            background="var(--gray-2)",
                            width="100%",
                            margin_top="3",
                        ),

                        spacing="3",
                        align="start",
                    ),
                    padding="4",
                    border="1px solid var(--purple-7)",
                    border_radius="lg",
                    background="var(--purple-1)",
                    width="100%",
                    margin_bottom="4",
                ),

                # How It Works Section
                rx.box(
                    rx.vstack(
                        rx.heading("🔍 How It Works", size="6", color="orange"),
                        rx.divider(margin_y="3"),

                        rx.vstack(
                            rx.text("The Core Concept:", weight="bold", size="4"),
                            rx.text(
                                "Sugar and ethanol are alternative uses of the SAME sugar cane harvest, not independent products.",
                                size="3",
                                color="gray",
                            ),

                            rx.heading("Decision Logic:", size="4", margin_top="4"),
                            rx.vstack(
                                rx.hstack(
                                    rx.text("1.", weight="bold"),
                                    rx.text("Calculate sugar production profit from the harvest", size="2"),
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.text("2.", weight="bold"),
                                    rx.text("Calculate ethanol production profit from the SAME harvest", size="2"),
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.text("3.", weight="bold"),
                                    rx.text("Compare profits: profit_difference = ethanol - sugar", size="2"),
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.text("4.", weight="bold"),
                                    rx.text("Recommend based on difference:", size="2"),
                                    spacing="2",
                                ),
                                rx.vstack(
                                    rx.text("• If difference > $500 → Recommend ETHANOL", size="2", color="blue"),
                                    rx.text("• If difference < -$500 → Recommend SUGAR", size="2", color="orange"),
                                    rx.text("• Otherwise → Recommend MIXED strategy", size="2", color="purple"),
                                    spacing="1",
                                    padding_left="4",
                                ),
                                spacing="2",
                                align="start",
                            ),

                            rx.heading("Shared Conditions:", size="4", margin_top="4"),
                            rx.text("These parameters are locked together because it's the same field:", size="2", color="gray"),
                            rx.vstack(
                                rx.text("• Cane yield (tons/hectare)", size="2"),
                                rx.text("• Sugar content (Brix %)", size="2"),
                                rx.text("• Quality (CCS)", size="2"),
                                rx.text("• Weather (temperature, rainfall)", size="2"),
                                rx.text("• Growing costs", size="2"),
                                spacing="1",
                                padding_left="3",
                            ),

                            spacing="3",
                            align="start",
                        ),

                        spacing="3",
                        align="start",
                    ),
                    padding="4",
                    border="1px solid var(--orange-7)",
                    border_radius="lg",
                    background="var(--orange-1)",
                    width="100%",
                    margin_bottom="4",
                ),

                # Mock Data Generation Explanation
                rx.box(
                    rx.vstack(
                        rx.heading("🧪 How Mock Data is Generated & Calculated", size="6", color="teal"),
                        rx.divider(margin_y="3"),

                        rx.text(
                            "The synthetic dataset is created in model.py → generate_unified_sugarcane_data(). "
                            "A fixed random seed (np.random.seed(42)) ensures the same data is reproduced every run. "
                            "Below is the step-by-step breakdown for the Ethanol dataset.",
                            size="3", color="gray", margin_bottom="3",
                        ),

                        # Step 1: Raw inputs
                        rx.box(
                            rx.vstack(
                                rx.text("Step 1 — Generate Raw Input Columns (Random Sampling)", weight="bold", size="3"),
                                rx.divider(margin_y="2"),
                                rx.vstack(
                                    rx.hstack(
                                        rx.badge("ethanol_price", color_scheme="teal"),
                                        rx.text("np.random.uniform(0.50, 0.85)  →  random price between $0.50 – $0.85 per liter", size="2"),
                                        spacing="2", align="center",
                                    ),
                                    rx.hstack(
                                        rx.badge("crude_oil_price", color_scheme="teal"),
                                        rx.text("np.random.uniform(60, 100)  →  random price between $60 – $100 per barrel", size="2"),
                                        spacing="2", align="center",
                                    ),
                                    rx.hstack(
                                        rx.badge("gasoline_price", color_scheme="teal"),
                                        rx.text("np.random.uniform(2.0, 3.2)  →  random price between $2.00 – $3.20 per gallon", size="2"),
                                        spacing="2", align="center",
                                    ),
                                    rx.hstack(
                                        rx.badge("ccs_quality", color_scheme="teal"),
                                        rx.text("np.random.normal(11.5, 1.0), clipped to [9.0, 14.0]  →  Commercial Cane Sugar quality index", size="2"),
                                        spacing="2", align="center",
                                    ),
                                    rx.hstack(
                                        rx.badge("fermentation_efficiency", color_scheme="teal"),
                                        rx.text("np.random.uniform(0.88, 0.96)  →  88% – 96% sugar-to-ethanol conversion rate", size="2"),
                                        spacing="2", align="center",
                                    ),
                                    rx.hstack(
                                        rx.badge("cane_yield_tons_per_hectare", color_scheme="gray"),
                                        rx.text("np.random.normal(80, 15), clipped to [40, 120]  →  tons of cane harvested per hectare", size="2"),
                                        spacing="2", align="center",
                                    ),
                                    rx.hstack(
                                        rx.badge("sugar_content_brix", color_scheme="gray"),
                                        rx.text("np.random.normal(14, 2), clipped to [10, 18]  →  sugar % in cane (Brix scale)", size="2"),
                                        spacing="2", align="center",
                                    ),
                                    rx.hstack(
                                        rx.badge("plantation_cost_per_hectare", color_scheme="gray"),
                                        rx.text("np.random.normal(2000, 300)  →  fixed growing cost in $ per hectare", size="2"),
                                        spacing="2", align="center",
                                    ),
                                    rx.hstack(
                                        rx.badge("ethanol_processing_cost_per_ton_cane", color_scheme="gray"),
                                        rx.text("np.random.normal(25, 5)  →  fermentation + distillation cost per ton of cane", size="2"),
                                        spacing="2", align="center",
                                    ),
                                    rx.hstack(
                                        rx.badge("bagasse_value_per_ton", color_scheme="gray"),
                                        rx.text("np.random.uniform(15, 35)  →  sale price of bagasse (cane fibre) byproduct", size="2"),
                                        spacing="2", align="center",
                                    ),
                                    spacing="2", align="start",
                                ),
                            ),
                            padding="4",
                            border="1px solid var(--teal-5)",
                            border_radius="md",
                            background="var(--teal-1)",
                            width="100%",
                            margin_bottom="3",
                        ),

                        # Step 2: Intermediate calculations
                        rx.box(
                            rx.vstack(
                                rx.text("Step 2 — Calculate Ethanol Production Yield", weight="bold", size="3"),
                                rx.divider(margin_y="2"),
                                rx.code(
                                    "ethanol_liters_per_hectare =\n"
                                    "    cane_yield_tons_per_hectare\n"
                                    "    × (sugar_content_brix / 100)\n"
                                    "    × fermentation_efficiency\n"
                                    "    × 650   # ~650 liters per ton of fermentable sugar",
                                    display="block", white_space="pre", font_size="13px",
                                ),
                                rx.text(
                                    "Example: 80 t/ha × 0.14 × 0.92 × 650 = 6,697 liters/ha",
                                    size="2", color="gray", margin_top="2",
                                ),
                            ),
                            padding="4",
                            border="1px solid var(--teal-5)",
                            border_radius="md",
                            background="var(--teal-1)",
                            width="100%",
                            margin_bottom="3",
                        ),

                        # Step 3: Byproduct
                        rx.box(
                            rx.vstack(
                                rx.text("Step 3 — Calculate Bagasse Byproduct Revenue", weight="bold", size="3"),
                                rx.divider(margin_y="2"),
                                rx.code(
                                    "bagasse_tons_per_hectare = cane_yield_tons_per_hectare × 0.28\n"
                                    "  # ~28% of cane mass becomes bagasse (fibrous residue)\n\n"
                                    "ethanol_byproduct_revenue = bagasse_tons_per_hectare × bagasse_value_per_ton",
                                    display="block", white_space="pre", font_size="13px",
                                ),
                                rx.text(
                                    "Example: 80 × 0.28 = 22.4 tons bagasse × $25/ton = $560 byproduct revenue",
                                    size="2", color="gray", margin_top="2",
                                ),
                            ),
                            padding="4",
                            border="1px solid var(--teal-5)",
                            border_radius="md",
                            background="var(--teal-1)",
                            width="100%",
                            margin_bottom="3",
                        ),

                        # Step 4: Weather penalty
                        rx.box(
                            rx.vstack(
                                rx.text("Step 4 — Apply Weather Penalty", weight="bold", size="3"),
                                rx.divider(margin_y="2"),
                                rx.code(
                                    "weather_penalty = 0\n"
                                    "weather_penalty += clip(|avg_temp - 26| × 2,  0, 15)\n"
                                    "weather_penalty += clip(|rainfall_mm - 1200| × 0.01, 0, 10)\n"
                                    "# Optimal: 26°C and 1200mm rainfall — deviations reduce profit",
                                    display="block", white_space="pre", font_size="13px",
                                ),
                                rx.text(
                                    "Example: temp=28°C → penalty += |28-26|×2 = 4; rainfall=1000mm → penalty += |1000-1200|×0.01 = 2 → total penalty = $6",
                                    size="2", color="gray", margin_top="2",
                                ),
                            ),
                            padding="4",
                            border="1px solid var(--teal-5)",
                            border_radius="md",
                            background="var(--teal-1)",
                            width="100%",
                            margin_bottom="3",
                        ),

                        # Step 5: Profit per hectare
                        rx.box(
                            rx.vstack(
                                rx.text("Step 5 — Calculate Ethanol Profit per Hectare", weight="bold", size="3"),
                                rx.divider(margin_y="2"),
                                rx.code(
                                    "ethanol_revenue = ethanol_liters_per_hectare × ethanol_price_per_liter\n\n"
                                    "ethanol_processing_cost =\n"
                                    "    cane_yield_tons_per_hectare × ethanol_processing_cost_per_ton_cane\n\n"
                                    "ethanol_profit_per_hectare =\n"
                                    "    ethanol_revenue\n"
                                    "  + ethanol_byproduct_revenue\n"
                                    "  - ethanol_processing_cost\n"
                                    "  - plantation_cost_per_hectare\n"
                                    "  - weather_penalty",
                                    display="block", white_space="pre", font_size="13px",
                                ),
                                rx.text(
                                    "Example: 6697L × $0.65 = $4,353 revenue + $560 byproduct − (80×$25=$2,000 processing) − $2,000 plantation − $6 weather = $907/ha",
                                    size="2", color="gray", margin_top="2",
                                ),
                            ),
                            padding="4",
                            border="1px solid var(--teal-5)",
                            border_radius="md",
                            background="var(--teal-1)",
                            width="100%",
                            margin_bottom="3",
                        ),

                        # Step 6: Final target
                        rx.box(
                            rx.vstack(
                                rx.text("Step 6 — Compute Target Column (What the ML Model Predicts)", weight="bold", size="3"),
                                rx.divider(margin_y="2"),
                                rx.code(
                                    "target_ethanol_profit_per_1000_liter =\n"
                                    "    (ethanol_profit_per_hectare / ethanol_liters_per_hectare) × 1000\n\n"
                                    "# Then ±8% random noise is applied to simulate real-world variance:\n"
                                    "ethanol_profit_per_hectare *= np.random.normal(1, 0.08)",
                                    display="block", white_space="pre", font_size="13px",
                                ),
                                rx.text(
                                    "Example: ($907 / 6697L) × 1000 = $135.4 profit per 1000 liters. "
                                    "This is the TARGET the ML model learns to predict from the 5 input features above.",
                                    size="2", color="gray", margin_top="2",
                                ),
                            ),
                            padding="4",
                            border="2px solid var(--teal-7)",
                            border_radius="md",
                            background="var(--teal-2)",
                            width="100%",
                            margin_bottom="3",
                        ),

                        # Summary formula
                        rx.box(
                            rx.vstack(
                                rx.text("Summary Formula", weight="bold", size="3"),
                                rx.divider(margin_y="2"),
                                rx.code(
                                    "target_ethanol_profit_per_1000_liter =\n"
                                    "  [\n"
                                    "    (yield × brix% × efficiency × 650 × ethanol_price)   ← ethanol revenue\n"
                                    "  + (yield × 0.28 × bagasse_price)                         ← byproduct\n"
                                    "  - (yield × processing_cost)                              ← processing\n"
                                    "  - plantation_cost                                         ← growing cost\n"
                                    "  - weather_penalty                                         ← climate impact\n"
                                    "  ] / (yield × brix% × efficiency × 650) × 1000",
                                    display="block", white_space="pre", font_size="13px",
                                ),
                            ),
                            padding="4",
                            border="1px solid var(--gray-5)",
                            border_radius="md",
                            background="var(--gray-2)",
                            width="100%",
                        ),

                        spacing="3",
                        align="start",
                    ),
                    padding="4",
                    border="1px solid var(--teal-7)",
                    border_radius="lg",
                    background="var(--teal-1)",
                    width="100%",
                    margin_bottom="4",
                ),

                # Additional Documentation Links
                rx.box(
                    rx.vstack(
                        rx.heading("📖 Additional Documentation Files", size="6"),
                        rx.divider(margin_y="3"),

                        rx.text("For more detailed information, check these markdown files in your project:", size="3"),

                        rx.vstack(
                            rx.hstack(
                                rx.text("📄", size="4"),
                                rx.vstack(
                                    rx.text("DOCUMENTATION_INDEX.md", weight="bold"),
                                    rx.text("Navigation guide for all documentation", size="2", color="gray"),
                                    spacing="1",
                                    align="start",
                                ),
                                spacing="3",
                                align="center",
                            ),
                            rx.hstack(
                                rx.text("📄", size="4"),
                                rx.vstack(
                                    rx.text("README_COMPLETE.md", weight="bold"),
                                    rx.text("Complete overview and implementation status", size="2", color="gray"),
                                    spacing="1",
                                    align="start",
                                ),
                                spacing="3",
                                align="center",
                            ),
                            rx.hstack(
                                rx.text("📄", size="4"),
                                rx.vstack(
                                    rx.text("QUICK_START.md", weight="bold"),
                                    rx.text("Get started in 5 minutes", size="2", color="gray"),
                                    spacing="1",
                                    align="start",
                                ),
                                spacing="3",
                                align="center",
                            ),
                            rx.hstack(
                                rx.text("📄", size="4"),
                                rx.vstack(
                                    rx.text("VISUAL_GUIDE.md", weight="bold"),
                                    rx.text("System diagrams and flowcharts", size="2", color="gray"),
                                    spacing="1",
                                    align="start",
                                ),
                                spacing="3",
                                align="center",
                            ),
                            rx.hstack(
                                rx.text("📄", size="4"),
                                rx.vstack(
                                    rx.text("REALISTIC_DECISION_MODEL.md", weight="bold"),
                                    rx.text("Complete technical explanation", size="2", color="gray"),
                                    spacing="1",
                                    align="start",
                                ),
                                spacing="3",
                                align="center",
                            ),
                            rx.hstack(
                                rx.text("📄", size="4"),
                                rx.vstack(
                                    rx.text("IMPLEMENTATION_SUMMARY.md", weight="bold"),
                                    rx.text("Developer reference and technical details", size="2", color="gray"),
                                    spacing="1",
                                    align="start",
                                ),
                                spacing="3",
                                align="center",
                            ),
                            spacing="3",
                            align="start",
                        ),

                        spacing="3",
                        align="start",
                    ),
                    padding="4",
                    border="1px solid var(--gray-7)",
                    border_radius="lg",
                    background="var(--gray-2)",
                    width="100%",
                ),

                spacing="4",
                width="100%",
            ),

            spacing="4",
            width="100%",
            min_height="85vh",
        ),
        size="4",
    )


app = rx.App()
app.add_page(index)
app.add_page(decision_page, route="/decision")
app.add_page(explanation_page, route="/explanation")


# project aims to predict the revenue of a sugarcane plant based
# weather they need to produce more sugarcane
# or they need to cut down the production and buy it from other
# should they reuse the byproducts for other purposes
# or sell it to other industries
# or use it for generating power for their own plant
# or sell it to the grid
# we can use machine learning to predict the revenue based on
# historical data of sugarcane production
# weather data
# market prices
# government policies
# and other factors
# we can use regression models to predict the revenue
# and use the predictions to make informed decisions.