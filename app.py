# app.py
import streamlit as st  # ADD THIS IMPORT AT THE TOP
import pandas as pd
from data_prep import prepare_data
from competitor_monitoring import monitor_competitor_prices
from elasticity import calculate_elasticity
from segmentation import segment_customers
from pricing_model import DynamicPricingModel
from dashboard import generate_pricing_dashboard

# Load and prepare data
@st.cache_data
def load_data():
    df = prepare_data()
    
    # Calculate elasticity
    elasticities = df.groupby('product_id').apply(calculate_elasticity)
    df = df.merge(elasticities.rename('product_elasticity'), on='product_id')
    
    # Customer segmentation
    df = segment_customers(df)
    
    # Competitor monitoring
    df = df.groupby('product_id').apply(monitor_competitor_prices).reset_index(drop=True)
    return df

# Main app
def main():
    st.title("Dynamic Pricing Dashboard")
    
    df = load_data()
    pricing_model = DynamicPricingModel()
    pricing_model.train(df)
    
    # Product selection
    product_id = st.selectbox("Select Product", df['product_id'].unique())
    product_df = df[df['product_id'] == product_id]
    
    # Recommendation
    latest_data = product_df.iloc[[-1]]
    if st.button("Generate Price Recommendation"):
        price = pricing_model.recommend_price(product_id, latest_data)
        st.success(f"Recommended price: ${price:.2f}")
    
    # Dashboard
    st.pyplot(generate_pricing_dashboard(product_df))

if __name__ == "__main__":
    main()