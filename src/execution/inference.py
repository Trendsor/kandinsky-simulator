import pandas as pd

def predict(model, input_data, feature_columns):
    """
    Use the model to make predictions.

    Args:
        model: The loaded model.
        input_data (pd.DataFrame): The input data for prediction.
        feature_columns (list): List of feature column names used for training.

    Returns:
        Predictions as a pandas DataFrame.
    """
    try:
        # Filter the input data to include only the necessary features
        filtered_data = input_data[feature_columns]
        
        # Use the model to make predictions
        predictions = model.predict(filtered_data)
        
        # Return predictions as a DataFrame
        return pd.DataFrame(predictions, columns=["predictions"])
    except KeyError as e:
        raise ValueError(f"Missing required columns in input data: {e}")
    except Exception as e:
        raise RuntimeError(f"Error during prediction: {e}")