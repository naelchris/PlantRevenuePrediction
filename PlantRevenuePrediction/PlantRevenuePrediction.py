"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config


class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(

            # TODO : create the Header called Sugar Cane Plant Revenue Prediction

            # lets create a textbox fields to enter amount of sugarcane produced per tons



            rx.heading("Welcome to Reflex!", size="9"),
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
            spacing="5",
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