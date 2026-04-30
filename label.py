import pandas as pd
import numpy as np

sensor = pd.read_csv("Processed/sensor_featured.csv")
sensor["timestamp"] = pd.to_datetime(sensor["timestamp"]).dt.tz_localize(None)

irrig = pd.read_csv("Data/irrigation_log_rows.csv")
irrig["irrigated_at"] = pd.to_datetime(irrig["irrigated_at"]).dt.tz_localize(None)

sensor = sensor.sort_values("timestamp")
irrig = irrig.sort_values("irrigated_at")

sensor["label"] = 0


for t in irrig["irrigated_at"]:
    start = t - pd.Timedelta(minutes=120)

    mask = (
        (sensor["timestamp"] >= start) &
        (sensor["timestamp"] <= t)
    )

    sensor.loc[mask, "label"] = 1

sensor["irrigation_event"] = 0

irrig_times = set(irrig["irrigated_at"].dt.floor("10min"))
sensor_times = sensor["timestamp"].dt.floor("10min")

sensor.loc[
    sensor_times.isin(irrig_times),
    "irrigation_event"
] = 1
sensor = sensor.drop(columns=["irrigation_event"], errors="ignore")

sensor.to_csv("Processed/sensor_labeled.csv", index=False)

print("Hoàn thành")