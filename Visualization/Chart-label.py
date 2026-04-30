import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../Processed/sensor_labeled.csv")

counts = df["label"].value_counts().sort_index()
total = len(df)

distribution = pd.DataFrame({
    "Nhãn": counts.index,
    "Số lượng bản ghi": counts.values,
    "Tỷ lệ (%)": (counts.values / total * 100).round(2)
})

print(distribution)

distribution.to_csv("label_distribution_table.csv", index=False)

plt.figure(figsize=(6,5), dpi=200)

bars = plt.bar(distribution["Nhãn"].astype(str), distribution["Số lượng bản ghi"])

plt.xlabel("Nhãn", fontsize=12)
plt.ylabel("Số lượng bản ghi", fontsize=12)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + total*0.01, int(yval),
             ha='center', fontsize=11)

plt.tight_layout()
plt.savefig("label_distribution.png", dpi=500)
plt.show()

print("Hoàn thành")