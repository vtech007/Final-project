import sys
st.write(sys.executable, sys.version)  # Verify Python environment

# app.py
import streamlit as st  # MUST BE AT THE VERY TOP
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
    elasticities = df.groupby('product_id', group_keys=False).apply(calculate_elasticity)
    df = df.merge(elasticities.rename('product_elasticity'), on='product_id')
    
    # Customer segmentation
    df = segment_customers(df)
    
    # Competitor monitoring
    df = df.groupby('product_id', group_keys=False).apply(monitor_competitor_prices).reset_index(drop=True)
    return df

# Main app
def main():
    st.title("Dynamic Pricing Dashboard")
    
    try:
        df = load_data()
        pricing_model = DynamicPricingModel()
        pricing_model.train(df)
        
        # Product selection
        product_ids = df['product_id'].unique()
        if len(product_ids) == 0:
            st.error("No products found in dataset")
            return
            
        product_id = st.selectbox("Select Product", product_ids)
        product_df = df[df['product_id'] == product_id]
        
        if len(product_df) == 0:
            st.error(f"No data found for product {product_id}")
            return
            
        # Recommendation
        latest_data = product_df.iloc[[-1]]
        if st.button("Generate Price Recommendation"):
            try:
                price = pricing_model.recommend_price(product_id, latest_data)
                if price is None:
                    st.warning("No model available for this product")
                else:
                    st.success(f"Recommended price: ${price:.2f}")
            except Exception as e:
                st.error(f"Price recommendation failed: {str(e)}")
        
        # Dashboard
        try:
            st.pyplot(generate_pricing_dashboard(product_df))
        except Exception as e:
            st.error(f"Failed to generate dashboard: {str(e)}")
            
    except Exception as e:
        st.error(f"Application error: {str(e)}")

if __name__ == "__main__":
    main()