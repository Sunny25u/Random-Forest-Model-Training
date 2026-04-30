import pandas as pd
import numpy as np

df = pd.read_csv("Processed/sensor_clean.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.tz_localize(None)

df = df.sort_values("timestamp")
df = df.set_index("timestamp")

df = df.resample("10min").mean()

df["soil_moisture"] = df["soil_moisture"].ffill(limit=2)
df["air_temperature"] = df["air_temperature"].ffill(limit=2)
df["air_humidity"] = df["air_humidity"].ffill(limit=2)

df = df.dropna()
df = df.reset_index()

def calculate_vpd(temp, humidity):
    es = 0.6108 * np.exp((17.27 * temp) / (temp + 237.3))
    ea = es * (humidity / 100.0)
    return es - ea

df["VPD"] = calculate_vpd(df["air_temperature"], df["air_humidity"])

df["hour"] = df["timestamp"].dt.hour
df["hour_sin"] = np.sin(2*np.pi*df["hour"]/24)
df["hour_cos"] = np.cos(2*np.pi*df["hour"]/24)

df["soil_diff_1"] = df["soil_moisture"].diff(1)
df["soil_diff_3"] = df["soil_moisture"].diff(3)

start_date = pd.to_datetime("2026-01-12")
df["day"] = (df["timestamp"] - start_date).dt.days

def get_stage(d):
    if d < 25:
        return 0
    elif d < 50:
        return 1
    else:
        return 2

df["growth_stage"] = df["day"].apply(get_stage)

df = df.dropna()
df = df[[
    "timestamp",
    "soil_moisture",
    "air_temperature",
    "air_humidity",
    "VPD",
    "hour_sin",
    "hour_cos",
    "soil_diff_1",
    "soil_diff_3",
    "growth_stage"
]]

df.to_csv("Processed/sensor_featured.csv", index=False)