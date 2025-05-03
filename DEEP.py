from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

X_all, y_all = [], []

for code_name, df in load_all_data("코딩").items():
    try:
        X, y = make_features_labels(df)
        X_all.append(X)
        y_all.append(y)
    except Exception as e:
        print(f"{code_name} 처리 중 오류: {e}")

X = pd.concat(X_all)
y = pd.concat(y_all)

# 학습 및 검증 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)

# 모델 학습
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

results = []

for code_name, df in load_all_data("코딩").items():
    try:
        X_pred, _ = make_features_labels(df)
        last_data = X_pred.iloc[[-1]]  # 가장 최근 데이터 한 줄

        prob = model.predict_proba(last_data)[0][1]
        results.append((code_name, prob))
    except:
        continue

# 상승 확률 높은 순 정렬
top10 = sorted(results, key=lambda x: x[1], reverse=True)[:10]

for code, prob in top10:
    print(f"{code}: 상승 확률 {prob:.2%}")