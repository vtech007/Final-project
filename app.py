# app.py
# ... existing imports ...

@st.cache_data
def load_data():
    df = prepare_data()
    
    # Calculate elasticity
    elasticities = df.groupby('product_id').apply(calculate_elasticity)
    df = df.merge(elasticities.rename('product_elasticity'), on='product_id')
    
    # Customer segmentation
    df = segment_customers(df)
    
    # Competitor monitoring - reset index after groupby
    df = df.groupby('product_id').apply(monitor_competitor_prices).reset_index(drop=True)
    
    return df

# ... rest of the code ...