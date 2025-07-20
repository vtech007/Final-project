# elasticity.py
import numpy as np

def calculate_elasticity(product_df):
    X = product_df[['unit_price', 'qty']].values
    if len(X) > 1:
        price_changes = np.diff(X[:, 0]) / X[:-1, 0]
        quantity_changes = np.diff(X[:, 1]) / X[:-1, 1]
        valid_mask = (~np.isinf(price_changes)) & (~np.isnan(price_changes))
        elasticity = np.median(quantity_changes[valid_mask] / price_changes[valid_mask])
        return elasticity
    return 0