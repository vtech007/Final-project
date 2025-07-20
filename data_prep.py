import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.arima.model import ARIMA
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('retail_price.csv')

# Convert date column to datetime
df['month_year'] = pd.to_datetime(df['month_year'], format='%d-%m-%Y')

# Feature engineering
df['price_change'] = df.groupby('product_id')['unit_price'].pct_change()
df['demand_change'] = df.groupby('product_id')['qty'].pct_change()
df['price_elasticity'] = df['demand_change'] / df['price_change']
df['comp_price_diff'] = df['unit_price'] - df[['comp_1', 'comp_2', 'comp_3']].mean(axis=1)
df['profit_margin'] = (df['unit_price'] - df['fp1']) / df['unit_price']

# Handle infinite values from division
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.fillna(0, inplace=True)

# Segment products by category and price elasticity
df['elasticity_category'] = pd.cut(df['price_elasticity'], 
                                  bins=[-np.inf, -1.5, -0.5, 0.5, 1.5, np.inf],
                                  labels=['Highly Elastic', 'Elastic', 'Neutral', 
                                          'Inelastic', 'Highly Inelastic'])

# Save prepared dataset
df.to_csv('prepared_retail_pricing.csv', index=False)