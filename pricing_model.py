# pricing_model.py
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

class DynamicPricingModel:
    def __init__(self):
        self.models = {}
        self.elasticity_thresholds = {
            'Highly Elastic': 0.9,
            'Elastic': 0.95,
            'Neutral': 1.0,
            'Inelastic': 1.05,
            'Highly Inelastic': 1.1
        }
    
    def train(self, product_df):
        """Train a pricing model for each product"""
        # Reset index to avoid index-column name conflicts
        product_df = product_df.reset_index(drop=True)
        
        # Create lag_price feature
        product_df['lag_price'] = product_df.groupby('product_id')['unit_price'].shift(1)
        
        for product_id, data in product_df.groupby('product_id'):
            if len(data) > 12:  # Need sufficient data
                try:
                    # Drop rows with missing lag_price
                    data = data.dropna(subset=['lag_price'])
                    
                    # Features: lagged price, competitor prices, seasonality, elasticity
                    X = data[['lag_price', 'comp_1', 'comp_2', 'comp_3', 
                             'month', 'product_elasticity', 'holiday']]
                    y = data['unit_price']
                    
                    # Train/test split
                    X_train, X_test, y_train, y_test = train_test_split(
                        X, y, test_size=0.2, shuffle=False)
                    
                    # Model training
                    model = RandomForestRegressor(n_estimators=100, random_state=42)
                    model.fit(X_train, y_train)
                    
                    # Store model
                    self.models[product_id] = model
                except Exception as e:
                    print(f"Error training model for {product_id}: {str(e)}")
                    continue
    
    def recommend_price(self, product_id, current_data):
        """Generate price recommendation for a product"""
        if product_id not in self.models:
            return None
        
        model = self.models[product_id]
        
        # Get elasticity category
        elasticity_cat = current_data['elasticity_category'].values[0]
        
        # Base prediction
        recommended_price = model.predict(current_data[['lag_price', 'comp_1', 'comp_2', 
                                                     'comp_3', 'month', 
                                                     'product_elasticity', 'holiday']])
        
        # Adjust based on elasticity
        elasticity_factor = self.elasticity_thresholds.get(elasticity_cat, 1.0)
        adjusted_price = recommended_price * elasticity_factor
        
        # Consider profit margins (don't go below cost)
        min_price = current_data['fp1'].values[0] * 1.1  # 10% above cost
        adjusted_price = max(adjusted_price, min_price)
        
        return adjusted_price[0]