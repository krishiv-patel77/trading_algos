'''
This file has many useful functions. Upload more as needed and add proper documentation and ensure they work before uploading.
'''

def save_to_csv(df, file_name, folder_name='data_folder'):
    import os
    
    # Create folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Save DataFrame to CSV file inside the folder
    df.to_csv(f'{folder_name}/{file_name}.csv', index=False)



def get_data_metatrader(start_date, end_date, timeframe):
    import MetaTrader5 as mt5
    import pandas as pd
    from datetime import datetime
    import pytz
    
    # Initialize MetaTrader 5 connection
    mt5.initialize()

    # Set timezone to UTC
    timezone = pytz.timezone("Etc/UTC")

    # Convert start_date and end_date to datetime objects if they are strings
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # Ensure the dates are in UTC timezone
    start_date = timezone.localize(start_date)
    end_date = timezone.localize(end_date)

    # Validate the timeframe argument
    valid_timeframes = {
        'M1': mt5.TIMEFRAME_M1,
        'M5': mt5.TIMEFRAME_M5,
        'M15': mt5.TIMEFRAME_M15,
        'M30': mt5.TIMEFRAME_M30,
        'H1': mt5.TIMEFRAME_H1,
        'H4': mt5.TIMEFRAME_H4,
        'D1': mt5.TIMEFRAME_D1,
        'W1': mt5.TIMEFRAME_W1,
        'MN1': mt5.TIMEFRAME_MN1
    }

    if timeframe not in valid_timeframes:
        raise ValueError(f"Invalid timeframe. Valid options are {list(valid_timeframes.keys())}")

    # Get historical rates for EURUSD in the provided timeframe
    rates = mt5.copy_rates_range("EURUSD", valid_timeframes[timeframe], start_date, end_date)
    
    # Convert the rates to a DataFrame
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')

    return df

