import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, average_precision_score

try:
    test = pd.read_csv('../Processed/test.csv')
    model = joblib.load('../Models/irrigation_model.pkl')
    print("--- Đã load dữ liệu và mô hình thành công ---")
except FileNotFoundError as e:
    print(f"Lỗi: Không tìm thấy file. Vui lòng kiểm tra lại đường dẫn. Chi tiết: {e}")
    exit()

X_test = test.drop(columns=['label'])
y_test = test['label']

cols_to_drop = ['id', 'timestamp', 'created_at']
X_test = X_test.drop(columns=cols_to_drop, errors='ignore')


y_probs = model.predict_proba(X_test)[:, 1]

fpr, tpr, thresholds_roc = roc_curve(y_test, y_probs)
auc_score = roc_auc_score(y_test, y_probs)

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {auc_score:.4f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate (FPR)')
plt.ylabel('True Positive Rate (TPR)')
plt.title('ROC Curve Analysis')
plt.legend(loc="lower right")
plt.grid(alpha=0.3)

precision, recall, thresholds_pr = precision_recall_curve(y_test, y_probs)
ap_score = average_precision_score(y_test, y_probs)

plt.subplot(1, 2, 2)
plt.plot(recall, precision, color='green', lw=2, label=f'PR curve (AP = {ap_score:.4f})')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend(loc="lower left")
plt.grid(alpha=0.3)

plt.tight_layout()

output_path = 'roc_auc_analysis.png'
plt.savefig(output_path, dpi=300)
print(f"--- Kết quả ROC-AUC: {auc_score:.4f} ---")
print(f"--- Đã lưu biểu đồ vào: {output_path} ---")
plt.show()