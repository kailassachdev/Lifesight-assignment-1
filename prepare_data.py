
import pandas as pd

def prepare_data():
    # Load the datasets
    business_df = pd.read_csv("Marketing Intelligence Dashboard/business.csv")
    facebook_df = pd.read_csv("Marketing Intelligence Dashboard/Facebook.csv")
    google_df = pd.read_csv("Marketing Intelligence Dashboard/Google.csv")
    tiktok_df = pd.read_csv("Marketing Intelligence Dashboard/TikTok.csv")

    # Add a 'source' column to each marketing DataFrame
    facebook_df['source'] = 'Facebook'
    google_df['source'] = 'Google'
    tiktok_df['source'] = 'TikTok'

    # Combine the marketing data
    marketing_df = pd.concat([facebook_df, google_df, tiktok_df])

    # Convert date columns to datetime objects
    marketing_df['date'] = pd.to_datetime(marketing_df['date'])
    business_df['date'] = pd.to_datetime(business_df['date'])

    # Merge the marketing and business data
    df = pd.merge(marketing_df, business_df, on='date', how='left')

    # Create new metrics
    df['cpc'] = df['spend'] / df['clicks']
    df['ctr'] = df['clicks'] / df['impression'] * 100
    df['roas'] = df['attributed revenue'] / df['spend']
    
    # Rename columns for clarity
    df.rename(columns={'# of orders': 'orders', '# of new orders': 'new_orders', 'new customers': 'new_customers', 'total revenue': 'total_revenue', 'gross profit': 'gross_profit'}, inplace=True)

    return df

if __name__ == '__main__':
    df = prepare_data()
    print(df.head())
    print(df.info())
    print(df.isnull().sum())
