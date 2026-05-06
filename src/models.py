import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

class AdOptimizer:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = None
        self.kmeans = KMeans(n_clusters=3, random_state=42)
    
    def train(self, df):
        # Features: spend, clicks, channel encoded
        df['channel_code'] = pd.Categorical(df['channel']).codes
        X = df[['spend', 'clicks', 'channel_code']]
        y = df['roi']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        self.model.fit(X_train, y_train)
        pred = self.model.predict(X_test)
        print(f"Model MAE: {mean_absolute_error(y_test, pred):.2f}")
    
    def predict_roi(self, spend, clicks, channel):
        channel_code = pd.Series([channel]).astype('category').cat.codes[0]
        return self.model.predict([[spend, clicks, channel_code]])[0]
    
    def optimize_budget(self, total_budget, channels=['Google Ads', 'Facebook']):
        # Simulate optimal allocation
        allocations = {}
        for ch in channels:
            pred_roi = np.random.uniform(2.5, 4.0)  # Mock high-ROI
            allocations[ch] = total_budget * (pred_roi / sum(np.random.uniform(2.5, 4.0, len(channels))))
        return allocations
    
    def detect_underperform(self, df):
        df['predicted_roi'] = df.apply(lambda row: self.predict_roi(row['spend'], row['clicks'], row['channel']), axis=1)
        under = df[df['roi'] < df['predicted_roi'] * 0.8]
        return under[['channel', 'spend', 'roi']]