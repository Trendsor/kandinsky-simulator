import pandas as pd

class RollingDataBuffer:
    def __init__(self, initial_data, window=200):
        """
        Initializes the rolling buffer.

        Args:
            initial_data (pd.DataFrame): Historical data to initialize the buffer.
            window (int): Rolling window size.
        """
        self.window = window
        self.data = initial_data[-window:]  # Keep only the last `window` rows

    def update(self, new_data):
        """
        Update the buffer with a new data entry and recalculate rolling metrics.

        Args:
            new_data (dict): New data point as a dictionary.

        Returns:
            pd.DataFrame: Updated buffer with rolling metrics.
        """
        try:
            # Debug: Check if new_data timestamp is tz-aware
            print(f"New data timestamp before conversion: {new_data['timestamp']}")
            new_data['timestamp'] = pd.Timestamp(new_data['timestamp']).tz_localize(None)
            print(f"New data timestamp after conversion: {new_data['timestamp']}")
                # Append the new entry
            new_row = pd.DataFrame([new_data])
            self.data = pd.concat([self.data, new_row], ignore_index=True)

            # Keep only the last `window` rows
            self.data = self.data[-self.window:]

            return self.data
        except Exception as e:
            raise ValueError(f"Error updating rolling buffer: {e}")