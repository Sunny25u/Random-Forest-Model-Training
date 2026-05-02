import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

train = pd.read_csv('Processed/train.csv')
test = pd.read_csv('Processed/test.csv')

features = [
    "soil_moisture",
    "air_temperature",
    "air_humidity",
    "VPD",
    "hour_sin",
    "hour_cos",
    "soil_diff_1",
    "soil_diff_3",
    "growth_stage"
]

X_train = train[features]
y_train = train['label']

X_test = test[features]
y_test = test['label']


model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    random_state=42,
    min_samples_leaf=1,
    class_weight={0: 1, 1: 4}
)

model.fit(X_train, y_train)


y_prob = model.predict_proba(X_test)[:, 1]
y_pred = (y_prob > 0.35).astype(int)


print("===== CONFUSION MATRIX =====")
cm = confusion_matrix(y_test, y_pred)
print(cm)

print("\n===== CLASSIFICATION REPORT =====")
print(classification_report(y_test, y_pred))


plt.figure(figsize=(5,4), dpi=150)
sns.heatmap(cm, annot=True, fmt='d')

plt.xlabel("Dự đoán")
plt.ylabel("Thực tế")

plt.tight_layout()
plt.savefig("confusion_matrix.png", dpi=400)
plt.show()


importance = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
}).sort_values(by="importance", ascending=False)

print("\n===== FEATURE IMPORTANCE =====")
print(importance)


joblib.dump(model, 'Models/irrigation_model_1.pkl')

print("Hoàn thành")