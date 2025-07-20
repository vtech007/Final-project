# elasticity.py
import numpy as np

def calculate_elasticity(product_df):
    """
    Calculate price elasticity of demand for each product
    with safe division and NaN handling
    """
    X = product_df[['unit_price', 'qty']].values
    if len(X) > 1:
        with np.errstate(divide='ignore', invalid='ignore'):
            price_changes = np.diff(X[:, 0]) / X[:-1, 0]
            quantity_changes = np.diff(X[:, 1]) / X[:-1, 1]
            elasticities = np.divide(quantity_changes, price_changes)
        
        # Filter invalid values
        valid_mask = np.isfinite(elasticities)
        if np.any(valid_mask):
            return np.median(elasticities[valid_mask])
    return 0  # Default for insufficient data