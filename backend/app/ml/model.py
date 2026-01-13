from sklearn.linear_model import LinearRegression
import numpy as np

class RiskForecastModel:
    def __init__(self):
        self.model = LinearRegression()

    def train(self, risks):
        X = np.arange(len(risks)).reshape(-1, 1)
        y = risks
        self.model.fit(X, y)

    def predict_next(self, steps=1):
        next_x = np.array([[len(self.model.coef_) + steps]])
        return float(self.model.predict(next_x)[0])