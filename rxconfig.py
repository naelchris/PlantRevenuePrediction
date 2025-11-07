import reflex as rx

config = rx.Config(
    app_name="PlantRevenuePrediction",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)