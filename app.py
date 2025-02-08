# -*- coding: utf-8 -*-
import sys
import pandas as pd
from yahoo_fin import stock_info

# Windows 환경에서 UTF-8 강제 설정 (출력 인코딩 문제 방지)
sys.stdout.reconfigure(encoding="utf-8")

def get_stock_data(symbol):
    """ 특정 주식의 현재 가격과 배당금 정보 가져오기 """
    try:
        # 현재 주가 가져오기 (소수점 2자리로 반올림)
        current_price = round(stock_info.get_live_price(symbol), 2)
        
        # 종목의 상세 정보 가져오기
        quote_table = stock_info.get_quote_table(symbol)
        
        # 배당금 정보 가져오기 (배당이 없는 종목도 있음)
        dividend_info = quote_table.get("Forward Dividend & Yield", "배당 없음")

    except Exception as e:
        # 데이터 조회 실패 시 기본 값 반환
        print(f"⚠ {symbol} 데이터 가져오기 오류: {e}")
        current_price = "데이터 없음"
        dividend_info = "데이터 없음"

    return {
        "종목": symbol,
        "현재 가격 (USD)": current_price,
        "배당금": dividend_info
    }

# 기본 종목 리스트 (테슬라, 애플, 엔비디아, 아마존, 구글, 코인베이스)
default_stocks = ["TSLA", "AAPL", "NVDA", "AMZN", "GOOGL", "COIN"]

# ✅ 유저 입력 받기 (무조건 Enter를 치면 바로 넘어감)
print('추가로 조회할 종목의 티커를 입력하세요 (쉼표로 구분, 없으면 그냥 Enter): ', end="", flush=True)
try:
    user_input = input().strip().upper()
except EOFError:
    user_input = ""

# ✅ 무조건 다음 단계로 넘어가게 처리
if not user_input:
    all_stocks = default_stocks
    print("\n✅ 기본 종목 리스트로 진행합니다.")
else:
    # 입력된 종목 리스트 변환 (대문자로 변환 & 공백 제거)
    additional_stocks = [stock.strip().upper() for stock in user_input.split(",") if stock.strip()]
    all_stocks = default_stocks + additional_stocks
    print(f"\n✅ 추가된 종목 리스트: {additional_stocks}")

# ✅ 모든 종목의 데이터 조회 후 표 형태로 출력
data_list = []
for stock in all_stocks:
    data_list.append(get_stock_data(stock))

# ✅ 데이터프레임으로 변환 후 출력
df = pd.DataFrame(data_list)

print("\n📊 주식 데이터 조회 결과:")
print(df.to_string(index=False))  # 인덱스 없이 깔끔하게 출력
