import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sensor = pd.read_csv("sensor_data_rows.csv")

sensor["timestamp"] = pd.to_datetime(sensor["timestamp"])

sensor = sensor.dropna()
sensor = sensor.drop_duplicates()

sensor = sensor[
    (sensor["soil_moisture"] >= 0) &
    (sensor["soil_moisture"] <= 100) &
    (sensor["air_temperature"] >= 0) &
    (sensor["air_temperature"] <= 50) &
    (sensor["air_humidity"] >= 0) &
    (sensor["air_humidity"] <= 100)
]

def remove_outliers(df, column):

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    df = df[(df[column] >= lower) & (df[column] <= upper)]

    return df

sensor = remove_outliers(sensor, "soil_moisture")
sensor = remove_outliers(sensor, "air_temperature")
sensor = remove_outliers(sensor, "air_humidity")

sensor["hour"] = sensor["timestamp"].dt.hour
sensor["day"] = sensor["timestamp"].dt.day
sensor["month"] = sensor["timestamp"].dt.month

sensor.to_csv("sensor_clean.csv", index=False)

print("Hoàn Thành")