import pandas as pd
from sklearn.model_selection import train_test_split

# Load dữ liệu
df = pd.read_csv("Processed/sensor_labeled.csv")

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Reset index (không cần sort time)
df = df.reset_index(drop=True)

# 🔥 Tạo cột stratify theo stage + label
df["stratify_col"] = (
    df["growth_stage"].astype(str) + "_" + df["label"].astype(str)
)

# 🔥 Random split 80/20
train, test = train_test_split(
    df,
    test_size=0.2,
    random_state=42,
    stratify=df["stratify_col"]
)

# Xóa cột phụ
train = train.drop(columns=["stratify_col"])
test = test.drop(columns=["stratify_col"])

# ================== CHECK ==================

print("TRAIN LABEL:")
print(train["label"].value_counts())
print("-" * 30)

print("TEST LABEL:")
print(test["label"].value_counts())
print("-" * 30)

print("TRAIN STAGE:")
print(train["growth_stage"].value_counts())
print("-" * 30)

print("TEST STAGE:")
print(test["growth_stage"].value_counts())
print("-" * 30)

# ================== SAVE ==================

train.to_csv("Processed/train.csv", index=False)
test.to_csv("Processed/test.csv", index=False)

print("Hoàn thành")