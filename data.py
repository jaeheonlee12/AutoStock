import pandas as pd
import os
from glob import glob

# 저장된 데이터 불러오기
def load_all_data(data_path):
    file_list = glob(os.path.join(data_path, "*.csv"))
    stock_data = {}

    for file in file_list:
        df = pd.read_csv(file)
        code_name = os.path.basename(file).replace(".csv", "")
        stock_data[code_name] = df
    return stock_data


def make_features_labels(df, window=60):
    df = df.copy()
    df['종가'] = df['현재가'].astype(float)

    # 수익률 계산
    df['future_return'] = df['종가'].shift(-window) / df['종가'] - 1
    df['label'] = (df['future_return'] > 0).astype(int)

    # 간단한 지표 예시
    df['ma5'] = df['종가'].rolling(window=5).mean()
    df['ma20'] = df['종가'].rolling(window=20).mean()
    df['volatility'] = df['종가'].pct_change().rolling(window=10).std()

    # 결측치 제거 및 라벨 존재하는 시점만
    df.dropna(inplace=True)
    return df[['ma5', 'ma20', 'volatility']], df['label']

