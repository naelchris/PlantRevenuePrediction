import reflex as rx

class State(rx.state):
    revenue: float = 0.0 # attribute revenue

    def load_revenue(self):
        #we can get from db or api
        self.revenue = 1000000.0
        return self.revenue
