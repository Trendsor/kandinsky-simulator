import pandas as pd

def predict(model, input_data):
    """
    Use the model to make predictions.

    Args:
        model: The loaded model.
        input_data (pd.DataFrame): The input data for prediction.

    Returns:
        Predictions as a pandas Dataframe.
    """
    return model.predict(input_data)