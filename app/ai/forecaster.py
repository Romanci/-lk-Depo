import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.erp_models import SalesOrder

class DemandForecaster:
    """
    Simple AI model for demand forecasting using Linear Regression.
    """
    def __init__(self):
        self.model = LinearRegression()

    def train_and_predict(self, historical_sales: list):
        if len(historical_sales) < 2:
            return None

        df = pd.DataFrame(historical_sales)
        df['date'] = pd.to_datetime(df['date'])
        df['days_from_start'] = (df['date'] - df['date'].min()).dt.days

        X = df[['days_from_start']]
        y = df['quantity']

        self.model.fit(X, y)

        next_date_days = df['days_from_start'].max() + 30
        prediction = self.model.predict(pd.DataFrame([[next_date_days]], columns=['days_from_start']))

        return max(0, prediction[0])

def get_ai_insight(db: Session, product_id: int):
    # Fetch historical sales data from the SalesOrder table
    orders = db.query(SalesOrder).filter(SalesOrder.product_id == product_id, SalesOrder.status == "completed").all()

    if not orders:
        history = [
            {'date': '2023-10-01', 'quantity': 50},
            {'date': '2023-11-01', 'quantity': 55},
            {'date': '2023-12-01', 'quantity': 65},
        ]
    else:
        history = [{'date': o.order_date.strftime('%Y-%m-%d'), 'quantity': o.quantity} for o in orders]

    forecaster = DemandForecaster()
    forecast = forecaster.train_and_predict(history)
    return {
        "product_id": product_id,
        "forecasted_demand_next_month": forecast,
        "data_source": "historical_orders" if orders else "mock_data"
    }
