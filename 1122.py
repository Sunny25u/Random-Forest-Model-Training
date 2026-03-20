import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu
df = pd.read_csv('sensor_labeled.csv')

X = df.drop(columns=['timestamp', 'label'])
y = df['label']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

from imblearn.over_sampling import SMOTE
smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

before_counts = y_train.value_counts().sort_index()
after_counts = y_train_smote.value_counts().sort_index()

fig, axes = plt.subplots(1, 2, figsize=(10,4))

bars1 = axes[0].bar(before_counts.index.astype(str), before_counts.values)
axes[0].set_title("Before SMOTE")
axes[0].set_xlabel("Nhãn")
axes[0].set_ylabel("Số lượng bản ghi")

for bar in bars1:
    yval = bar.get_height()
    axes[0].text(bar.get_x() + bar.get_width()/2, yval + 5, int(yval), ha='center')

bars2 = axes[1].bar(after_counts.index.astype(str), after_counts.values)
axes[1].set_title("After SMOTE")
axes[1].set_xlabel("Nhãn")
axes[1].set_ylabel("Số lượng bản ghi")

for bar in bars2:
    yval = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width()/2, yval + 5, int(yval), ha='center')

axes[0].set_xticks([0,1])
axes[0].set_xticklabels(["label = 0", "label = 1"])

axes[1].set_xticks([0,1])
axes[1].set_xticklabels(["label = 0", "label = 1"])

plt.tight_layout()
plt.savefig("smote.png", dpi=400)
plt.show()