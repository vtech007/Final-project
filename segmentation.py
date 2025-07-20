# segmentation.py
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def segment_customers(df):
    """
    Cluster customers based on purchasing behavior for personalized pricing
    """
    # Features for clustering
    features = df[['total_price', 'qty', 'weekend', 'holiday', 'product_score']]
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    
    # K-means clustering
    kmeans = KMeans(n_clusters=3, random_state=42)
    df['customer_segment'] = kmeans.fit_predict(scaled_features)
    
    # Name the segments
    segment_names = {
        0: 'Budget Conscious',
        1: 'Regular',
        2: 'Premium'
    }
    df['customer_segment'] = df['customer_segment'].map(segment_names)
    
    return df