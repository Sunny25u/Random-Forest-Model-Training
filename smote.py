import pandas as pd
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

df = pd.read_csv('sensor_labeled.csv')

X = df.drop(columns=['timestamp', 'label'])
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("TẬP HUẤN LUYỆN (TRƯỚC SMOTE):")
print(y_train.value_counts())
print("-" * 30)

smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

print("TẬP HUẤN LUYỆN (SAU SMOTE):")
print(y_train_smote.value_counts())
print("-" * 30)

print("TẬP KIỂM TRA:")
print(y_test.value_counts())

train_smote = pd.concat([X_train_smote, y_train_smote], axis=1)
test = pd.concat([X_test, y_test], axis=1)

train_smote.to_csv('train_smote.csv', index=False)
test.to_csv('test.csv', index=False)