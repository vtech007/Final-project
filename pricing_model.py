# pricing_model.py
# ... imports ...

class DynamicPricingModel:
    # ... __init__ ...
    
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

    # ... recommend_price remains the same ...