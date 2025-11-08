"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from .state import State


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            # Header
            rx.heading("Sugar Cane Plant Revenue Prediction", size="8"),

            # Input form
            rx.hstack(
                rx.vstack(
                    rx.box(rx.text("Sugar price ($/Ton)"), rx.input(type="number", value=700.0, on_change=State.set_sugar_price)),
                    rx.box(rx.text("Ethanol price ($/L)"), rx.input(type="number", value=0.5, on_change=State.set_ethanol_price)),
                    rx.box(rx.text("Bagasse value ($/Ton)"), rx.input(type="number", value=20.0, on_change=State.set_bagasse_value)),
                    rx.box(rx.text("Molasses value ($/Ton)"), rx.input(type="number", value=8.0, on_change=State.set_molasses_value)),
                    spacing=4,
                ),
                rx.vstack(
                    rx.box(rx.text("Avg plantation temp (°C)"), rx.input(type="number", value=26.0, on_change=State.set_avg_temp_plantation)),
                    rx.box(rx.text("Rainfall at harvest (mm)"), rx.input(type="number", value=150.0, on_change=State.set_rainfall_harvest)),
                    rx.box(rx.text("CCS quality (%)"), rx.input(type="number", value=11.5, on_change=State.set_ccs_quality)),
                    rx.box(rx.text("Harvest month"), rx.input(type="number", value=9, min=1, max=12, on_change=State.set_harvest_month)),
                    spacing=4,
                ),
                spacing=8,
            ),

            # Buttons
            rx.hstack(
                rx.button("Predict", on_click=State.predict_profit),
                rx.button("Start Training", on_click=State.start_training),
                spacing=4,
            ),

            # Result display
            rx.box(
                rx.text("Predicted net profit per ton:"),
                rx.heading(lambda: f"${State.predicted_profit:.2f}", size=6),
                rx.text(lambda: f"Training status: {State.training_status}"),
                padding="4",
                border_width="1px",
                border_radius="md",
            ),

            # Existing welcome content
            rx.heading("Welcome to Reflex!", size=9),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            spacing=5,
            justify="center",
            min_height="85vh",
        ),
    )


app = rx.App()
app.add_page(index)


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