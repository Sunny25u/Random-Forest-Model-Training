import pandas as pd

sensor = pd.read_csv("sensor_featured.csv")
irrigation = pd.read_csv("Data/irrigation_log_rows.csv")

sensor["timestamp"] = pd.to_datetime(sensor["timestamp"])
irrigation["irrigated_at"] = pd.to_datetime(irrigation["irrigated_at"])

sensor["label"] = 0

for t in irrigation["irrigated_at"]:
    mask = (sensor["timestamp"] >= t - pd.Timedelta(hours=2)) & (sensor["timestamp"] <= t)
    sensor.loc[mask, "label"] = 1

sensor.to_csv("sensor_labeled.csv", index=False)