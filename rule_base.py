import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# =========================
# LOAD
# =========================
test = pd.read_csv("Processed/test.csv")

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

X_test = test[features]
y_test = test["label"]

# =========================
# MODEL
# =========================
model = joblib.load("Models/irrigation_model_1.pkl")

y_prob = model.predict_proba(X_test)[:, 1]
y_pred_model = (y_prob > 0.35).astype(int)

# =========================
# RULE-BASED
# =========================
def rule_based(row):
    if row["growth_stage"] == 0 and row["soil_moisture"] < 70:
        return 1
    elif row["growth_stage"] == 1 and row["soil_moisture"] < 65:
        return 1
    elif row["growth_stage"] == 2 and row["soil_moisture"] < 60:
        return 1
    else:
        return 0

test["rule_pred"] = test.apply(rule_based, axis=1)
y_pred_rule = test["rule_pred"]

# =========================
# EVALUATE
# =========================
print("\n===== MODEL (Random Forest) =====")
cm_model = confusion_matrix(y_test, y_pred_model)
print(cm_model)
print(classification_report(y_test, y_pred_model))

print("\n===== RULE-BASED =====")
cm_rule = confusion_matrix(y_test, y_pred_rule)
print(cm_rule)
print(classification_report(y_test, y_pred_rule))

# =========================
# PLOT CONFUSION MATRIX (2 cái chung 1 hình)
# =========================
fig, axes = plt.subplots(1, 2, figsize=(10,4), dpi=150)

# --- MODEL ---
sns.heatmap(cm_model, annot=True, fmt='d', ax=axes[0])
axes[0].set_title("Random Forest")
axes[0].set_xlabel("Dự đoán")
axes[0].set_ylabel("Thực tế")
axes[0].set_xticklabels(["Không tưới", "Tưới"])
axes[0].set_yticklabels(["Không tưới", "Tưới"], rotation=0)

# --- RULE ---
sns.heatmap(cm_rule, annot=True, fmt='d', ax=axes[1])
axes[1].set_title("Rule-based")
axes[1].set_xlabel("Dự đoán")
axes[1].set_ylabel("Thực tế")
axes[1].set_xticklabels(["Không tưới", "Tưới"])
axes[1].set_yticklabels(["Không tưới", "Tưới"], rotation=0)

plt.tight_layout()
plt.savefig("confusion_compare.png", dpi=400)
plt.show()

# =========================
# SO SÁNH
# =========================
compare = pd.DataFrame({
    "Method": ["Random Forest", "Rule-based"],
    "Accuracy": [
        (y_pred_model == y_test).mean(),
        (y_pred_rule == y_test).mean()
    ]
})

print("\n===== COMPARISON =====")
print(compare)