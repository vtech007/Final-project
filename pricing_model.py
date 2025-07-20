# pricing_model.py
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

class DynamicPricingModel:
    # __init__ remains same...
    
    def train(self, product_df):
        # ... original training code ...
        # Add lag_price creation:
        product_df['lag_price'] = product_df.groupby('product_id')['unit_price'].shift(1)
        # ... rest of training code ...

    # recommend_price remains same...

# Remove standalone execution code at bottom