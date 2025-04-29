from pykiwoom.kiwoom import Kiwoom

# 키움 API 객체 생성
kiwoom = Kiwoom()

# 로그인 시도
kiwoom.CommConnect()

# 연결 여부 확인 (1: 연결됨, 0: 연결 안됨)
is_connected = kiwoom.GetConnectState()
print("연결 상태:", "정상 연결" if is_connected == 1 else "연결 실패")
