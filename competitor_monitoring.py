def monitor_competitor_prices(product_df, window=3):
    """
    Track competitor prices and identify significant deviations
    """
    # Calculate moving averages of competitor prices
    product_df['comp1_ma'] = product_df['comp_1'].rolling(window=window).mean()
    product_df['comp2_ma'] = product_df['comp_2'].rolling(window=window).mean()
    product_df['comp3_ma'] = product_df['comp_3'].rolling(window=window).mean()
    
    # Identify significant price changes (>10%)
    product_df['comp1_change'] = product_df['comp_1'].pct_change() > 0.1
    product_df['comp2_change'] = product_df['comp_2'].pct_change() > 0.1
    product_df['comp3_change'] = product_df['comp_3'].pct_change() > 0.1
    
    return product_df

# Remove the problematic line that was trying to process df