import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("sensor_featured.csv")
corr = df.corr(numeric_only=True)
plt.figure(figsize=(10,8))
sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5
)
plt.tight_layout()
plt.savefig("Heat.png", dpi=400)
plt.show()