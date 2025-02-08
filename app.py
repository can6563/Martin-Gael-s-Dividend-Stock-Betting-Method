# -*- coding: utf-8 -*-
import sys
import pandas as pd
from yahoo_fin import stock_info

sys.stdout.reconfigure(encoding="utf-8")  # Windows에서 UTF-8 강제 설정

def get_stock_data(symbol):
    """ 특정 주식의 현재 가격과 배당금 정보 가져오기 """
    try:
        current_price = round(stock_info.get_live_price(symbol), 2)
        quote_table = stock_info.get_quote_table(symbol)
        dividend_info = quote_table.get("Forward Dividend & Yield", "배당 없음")
    except Exception as e:
        print(f"⚠ {symbol} 데이터 가져오기 오류: {e}")
        current_price = "데이터 없음"
        dividend_info = "데이터 없음"

    return {
        "종목": symbol,
        "현재 가격 (USD)": current_price,
        "배당금": dividend_info
    }

default_stocks = ["TSLA", "AAPL", "NVDA", "AMZN", "GOOGL", "COIN"]

# ✅ 입력 대기 문제 해결: Enter 누르면 무조건 넘어가도록 처리
try:
    print('추가로 조회할 종목의 티커를 입력하세요 (쉼표로 구분, 없으면 그냥 Enter): ', end="", flush=True)
    user_input = input().strip().upper()
except EOFError:
    user_input = ""

if not user_input:
    all_stocks = default_stocks
    print("\n✅ 기본 종목 리스트로 진행합니다.")
else:
    additional_stocks = [stock.strip().upper() for stock in user_input.split(",") if stock.strip()]
    all_stocks = default_stocks + additional_stocks
    print(f"\n✅ 추가된 종목 리스트: {additional_stocks}")

data_list = []
for stock in all_stocks:
    data_list.append(get_stock_data(stock))

df = pd.DataFrame(data_list)

print("\n📊 주식 데이터 조회 결과:")
print(df.to_string(index=False))
