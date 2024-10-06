import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
import joblib
# Read the cleaned CSV file
file_path = './CLEAN_DATA .csv'  # Replace with your actual file path
cleaned_data = pd.read_csv(file_path)

# Split dataset into 'For Sale' and 'For Lease'
for_sale_data = cleaned_data[(cleaned_data['FOR_SALE'] == 1) & (cleaned_data['FOR_LEASE'] == 0)]
for_lease_data = cleaned_data[(cleaned_data['FOR_SALE'] == 0) & (cleaned_data['FOR_LEASE'] == 1)]

# Verify the split
print("For Sale Dataset:", for_sale_data.shape)
print("For Lease Dataset:", for_lease_data.shape)
print(cleaned_data['SURFACE'].shape)

def process_real_estate_data(df):
    # Exclude DEALER_NAME and DEALER_TEL from the dataset
    df = df.drop(['DEALER_NAME', 'DEALER_TEL', 'ADS_LINK', 'SITE', 'ID_CLIENT', 'LAT', 'LON', 'PHOTOS', 'PRICE_M2'], axis=1)
    
    # Step 3: Date-Based Features
    df['ADS_DATE'] = pd.to_datetime(df['ADS_DATE'])
    df['year'] = df['ADS_DATE'].dt.year
    df['month'] = df['ADS_DATE'].dt.month
    df['day'] = df['ADS_DATE'].dt.day
    df['day_of_week'] = df['ADS_DATE'].dt.dayofweek
    df['quarter'] = df['ADS_DATE'].dt.quarter

    # Step 4: Categorical Variables (One-Hot Encoding)
    categorical_features = ['LAND_TYPE', 'CITY', 'DISTRICT', 'WARD', 'STREET', 'LEGAL_STATUS', 'PRO_DIRECTION']
    df = pd.get_dummies(df, columns=categorical_features, drop_first=True)

    # Step 5: Numeric Features (Interaction Term and Outlier Handling)
    df['price_per_floor'] = df['PRICE'] / df['NB_FLOORS']
    
    def cap_outliers(df, column, lower_percentile=0.01, upper_percentile=0.99):
        lower_limit = df[column].quantile(lower_percentile)
        upper_limit = df[column].quantile(upper_percentile)
        df[column] = df[column].clip(lower=lower_limit, upper=upper_limit)
    
    for column in ['PRICE', 'SURFACE']:
        cap_outliers(df, column)
    
    # Step 6: Handle NaN and Infinity Values
    df.replace([np.inf, -np.inf], np.nan, inplace=True)  # Replace infinity values with NaN
    df.fillna(df.median(), inplace=True)  # Fill NaN values with the median of each column

    # Step 7: Feature Scaling (Exclude non-numeric features)
    non_numeric_cols = ['ADS_DATE']  # Add any other non-numeric columns that shouldn't be scaled
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    numeric_cols = [col for col in numeric_cols if col not in non_numeric_cols]
    
    standard_scaler = StandardScaler()
    min_max_scaler = MinMaxScaler()
    
    standardized_features = ['SURFACE']
    df[standardized_features] = standard_scaler.fit_transform(df[standardized_features])
    test=standard_scaler.transform([[290]])
    print(test)

    scaled_features = ['NB_FLOORS']
    df[scaled_features] = min_max_scaler.fit_transform(df[scaled_features])

    # Step 8: Feature Selection using Random Forest (Exclude non-numeric columns)
    # X = df.drop(['PRICE', 'ADS_DATE'], axis=1)  # Exclude non-numeric column 'ADS_DATE'
    # y = df['PRICE']
    
    # rf_model = RandomForestRegressor(random_state=42)
    # rf_model.fit(X, y)
    
    # feature_importances = pd.Series(rf_model.feature_importances_, index=X.columns).sort_values(ascending=False)
    # selected_features = feature_importances.index[:10]  # Select top 10 important features
    joblib.dump(standard_scaler, 'standard_scaler.joblib')
    joblib.dump(min_max_scaler, 'min_max_scaler.joblib')
    # Return processed DataFrame with selected features
    return None

# Apply the pipeline to For Sale and For Lease datasets
processed_for_sale_data = process_real_estate_data(for_sale_data)
# processed_for_lease_data = process_real_estate_data(for_lease_data)



# # Verify results
# print("Processed For Sale Data:")
# print("Processed For Lease Data:")
