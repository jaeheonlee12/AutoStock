from pykiwoom.kiwoom import Kiwoom
import pandas as pd
import time
import os

# 키움 API 객체 생성
kiwoom = Kiwoom()

# 로그인 시도
kiwoom.CommConnect()

# 연결 여부 확인 (1: 연결됨, 0: 연결 안됨)
is_connected = kiwoom.GetConnectState()
print("연결 상태:", "정상 연결" if is_connected == 1 else "연결 실패")

# 시장 전체 코드 가져오기
def get_all_codes():
    kospi = kiwoom.GetCodeListByMarket('0')
    kosdaq = kiwoom.GetCodeListByMarket('10')
    return kospi + kosdaq

# 종목 필터링: 현재가 및 시가총액 조건
def filter_stocks_by_price_and_market_cap(codes):
    filtered = []

    for code in codes:
        try:
            name = kiwoom.GetMasterCodeName(code)
            price = kiwoom.GetMasterLastPrice(code)  # 수정됨
            listed_stock = kiwoom.GetMasterListedStockCnt(code)
            market_cap = price * listed_stock

            if 800 <= price <= 20000 and 700_000_000_000 <= market_cap <= 3_000_000_000_000:
                filtered.append((code, name))
        except Exception as e:
            print(f"{code} 오류: {e}")
        time.sleep(0.25)

    return filtered

# 종목별 일봉 데이터 수집
def get_daily_chart(code, count=750):
    기준일자 = time.strftime("%Y%m%d")  # 오늘 날짜 자동 지정
    df = kiwoom.block_request("opt10081",
                              종목코드=code,
                              기준일자=기준일자,
                              수정주가구분=1,
                              output="주식일봉차트조회",
                              next=0)

    df = pd.DataFrame(df)
    df = df.sort_values(by='일자')
    return df.head(count)

# 전체 실행 함수
def run_data_collection():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    save_dir = os.path.join(desktop, "코딩")
    os.makedirs(save_dir, exist_ok=True)

    codes = get_all_codes()
    print(f"총 {len(codes)}개 종목 확인 중...")

    filtered = filter_stocks_by_price_and_market_cap(codes)
    print(f"조건에 맞는 종목 수: {len(filtered)}개")

    for code, name in filtered:
        try:
            df = get_daily_chart(code)
            file_path = os.path.join(save_dir, f"{code}_{name}.csv")
            df.to_csv(file_path, index=False)
            print(f"{name} ({code}) 저장 완료")
        except Exception as e:
            print(f"{name} ({code}) 데이터 수집 실패: {e}")
        time.sleep(0.3)  # 요청 제한 방지

# 실행
run_data_collection()