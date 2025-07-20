# app.py
# ... existing code ...

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