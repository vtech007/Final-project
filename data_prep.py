# data_prep.py
import pandas as pd
import numpy as np

def prepare_data():
    df = pd.read_csv('retail_price.csv')
    df['month_year'] = pd.to_datetime(df['month_year'], format='%d-%m-%Y')
    
    # Feature engineering
    df['price_change'] = df.groupby('product_id')['unit_price'].pct_change()
    df['demand_change'] = df.groupby('product_id')['qty'].pct_change()
    df['price_elasticity'] = df['demand_change'] / df['price_change']
    df['comp_price_diff'] = df['unit_price'] - df[['comp_1', 'comp_2', 'comp_3']].mean(axis=1)
    df['profit_margin'] = (df['unit_price'] - df['fp1']) / df['unit_price']
    
    # Handle infinite values
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.fillna(0, inplace=True)
    
    # Elasticity categories
    df['elasticity_category'] = pd.cut(df['price_elasticity'], 
                                      bins=[-np.inf, -1.5, -0.5, 0.5, 1.5, np.inf],
                                      labels=['Highly Elastic', 'Elastic', 'Neutral', 
                                              'Inelastic', 'Highly Inelastic'])
    
    # Add month feature
    df['month'] = df['month_year'].dt.month
    return df