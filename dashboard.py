# dashboard.py
import matplotlib.pyplot as plt
import seaborn as sns

def generate_pricing_dashboard(product_df):
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    
    # Plot 1: Price trends
    sns.lineplot(data=product_df, x='month_year', y='unit_price', label='Our Price', ax=axs[0, 0])
    sns.lineplot(data=product_df, x='month_year', y='comp_1', label='Competitor 1', ax=axs[0, 0])
    sns.lineplot(data=product_df, x='month_year', y='comp_2', label='Competitor 2', ax=axs[0, 0])
    sns.lineplot(data=product_df, x='month_year', y='comp_3', label='Competitor 3', ax=axs[0, 0])
    axs[0, 0].set_title('Price Trends Comparison')
    axs[0, 0].tick_params(axis='x', rotation=45)
    
    # Plot 2: Elasticity
    sns.barplot(data=product_df, x='elasticity_category', y='qty', ax=axs[0, 1])
    axs[0, 1].set_title('Demand by Elasticity Category')
    
    # Plot 3: Customer segments
    sns.boxplot(data=product_df, x='customer_segment', y='unit_price', ax=axs[1, 0])
    axs[1, 0].set_title('Price Distribution by Customer Segment')
    
    # Plot 4: Profit margins
    sns.scatterplot(data=product_df, x='unit_price', y='profit_margin', 
                    hue='elasticity_category', ax=axs[1, 1])
    axs[1, 1].set_title('Price vs Profit Margin')
    
    plt.tight_layout()
    return fig