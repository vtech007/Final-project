# pricing_model.py
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split  # ADD MISSING IMPORT
import pandas as pd

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
        # ... existing training code ...
    
    # ADD MISSING METHOD
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