import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sensor = pd.read_csv("sensor_clean.csv")
"""
print(sensor.shape)
print(sensor.head())
print(sensor.info())
"""
sensor["timestamp"] = pd.to_datetime(sensor["timestamp"])
#print(sensor.isnull().sum())
"""
duplicates = sensor.duplicated().sum()
print("Data:", duplicates)
sensor = sensor.drop_duplicates()
"""
"""
plt.figure(figsize=(8,5))
#sns.histplot(sensor["soil_moisture"], bins=25, kde=True)
#sns.histplot(sensor["air_temperature"], bins=25, kde=True)
sns.histplot(sensor["air_humidity"], bins=25, kde=True)
#plt.xlabel("Soil Moisture (%)")
plt.xlabel("Air Humidity (%)")
plt.ylabel("Frequency")
plt.grid(True)
plt.savefig("Air.png", dpi=400)
plt.show()
"""
plt.figure(figsize=(10,6))
data = [
    sensor["soil_moisture"],
    sensor["air_temperature"],
    sensor["air_humidity"]
]
labels = ["Soil Moisture", "Temperature", "Humidity"]
sns.boxplot(data=data)
plt.xticks([0,1,2], labels)
plt.ylabel("Value")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("Boxplot-clean.png", dpi=400)
plt.show()
