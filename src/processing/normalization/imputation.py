import pandas as pd
import numpy as np

def impute_missing_values(data):
    """
    Imputes missing values in the dataset:

    Args:
        data (dict or pd.DataFrame): Input data, either as a dictionary (from Kafka) or a poandas DataFrame.

    Returns:
        dict or pd.DataFrame: Data with missing values imputed.
    """
    # Convert dict to DataFrame is necessary
    if isinstance(data, dict):
        data = pd.DataFrame([data])

    # Separate numerical and categoirical columns
    numerical_cols = data.select_dtypes(include=[np.number]).columns
    categorical_cols = data.select_dtypes(include=["object"]).columns

    # Impute numerical columns with its mean
    for col in numerical_cols:
        if data [col].isnull().sum() > 0:
            data[col].fillna(data[col].mean(), incplace=True)
    
    # Impute categorical columns with its mode
    for col in categorical_cols:
        if data[col].isnull().sum() > 0:
            data[col].fillna(data[col].mode()[0], inplace=True)
    
    # Convert back to dict if the input was a dict
    if isinstance(data, pd.DataFrame):
        return data.to_dict(orient="records")[0] if len(data) == 1 else data.to_dict(orient="records")
    
    return data