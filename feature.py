import pandas as pd
import numpy as np

sensor = pd.read_csv("Processed/sensor_clean.csv")

sensor = sensor.sort_values(by=["month", "day", "hour"])

es = 0.6108 * np.exp((17.27 * sensor["air_temperature"]) / (sensor["air_temperature"] + 237.3))
ea = es * (sensor["air_humidity"] / 100)
sensor["VPD"] = es - ea

sensor["heat_index"] = sensor["air_temperature"] - (
    (0.55 - 0.0055 * sensor["air_humidity"]) *
    (sensor["air_temperature"] - 14.5)
)

sensor["sm_change"] = sensor["soil_moisture"].diff().fillna(0)

sensor["hour_sin"] = np.sin(2 * np.pi * sensor["hour"] / 24)
sensor["hour_cos"] = np.cos(2 * np.pi * sensor["hour"] / 24)

sensor["month_sin"] = np.sin(2 * np.pi * sensor["month"] / 12)
sensor["month_cos"] = np.cos(2 * np.pi * sensor["month"] / 12)

sensor = sensor.drop(columns=["hour", "month", "id"], errors="ignore")

sensor.to_csv("sensor_featured.csv", index=False)