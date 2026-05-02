import pandas as pd
from sklearn.model_selection import train_test_split


df = pd.read_csv("Processed/sensor_labeled.csv")

df["timestamp"] = pd.to_datetime(df["timestamp"])

df = df.reset_index(drop=True)

df["stratify_col"] = (
    df["growth_stage"].astype(str) + "_" + df["label"].astype(str)
)

train, test = train_test_split(
    df,
    test_size=0.2,
    random_state=42,
    stratify=df["stratify_col"]
)

train = train.drop(columns=["stratify_col"])
test = test.drop(columns=["stratify_col"])


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

train.to_csv("Processed/train.csv", index=False)
test.to_csv("Processed/test.csv", index=False)

print("Hoàn thành")