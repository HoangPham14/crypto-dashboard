import streamlit as st
import yfinance as yf
import ta
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Crypto Dashboard", page_icon="📈", layout="wide")

st.title("📈 Crypto Dashboard: Phân Tích Chỉ Báo Kỹ Thuật")

# Chọn Coin & Thời gian
coins = ["BTC-USD", "ETH-USD", "BNB-USD"]
symbol = st.selectbox("Chọn Coin", coins, index=0)

period = st.selectbox(
    "Chọn Khoảng Thời Gian",
    ["1mo", "3mo", "6mo", "1y", "2y"],
    index=2
)

# Tải dữ liệu
data = yf.download(symbol, period=period)
if data.empty:
    st.error("Không có dữ liệu! Hãy thử coin khác.")
    st.stop()

# Tính chỉ báo
close = data['Close'].squeeze()
data['MA20'] = close.rolling(window=20).mean()
data['RSI'] = ta.momentum.RSIIndicator(close, window=14).rsi()
macd = ta.trend.MACD(close)
data['MACD'] = macd.macd()
data['MACD_Signal'] = macd.macd_signal()

# Hiển thị bảng dữ liệu
st.subheader(f"Bảng Dữ Liệu {symbol}")
st.dataframe(data.tail(10))

# Vẽ biểu đồ giá + MA20
st.subheader("Biểu đồ Giá & MA20")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(data.index, close, label="Close Price")
ax.plot(data.index, data['MA20'], label="MA20")
ax.set_title(f"{symbol} - Price & MA20")
ax.legend()
st.pyplot(fig)

# Vẽ MACD
st.subheader("Biểu đồ MACD")
fig2, ax2 = plt.subplots(figsize=(12, 4))
ax2.plot(data.index, data['MACD'], label="MACD")
ax2.plot(data.index, data['MACD_Signal'], label="MACD Signal")
ax2.set_title(f"{symbol} - MACD")
ax2.legend()
st.pyplot(fig2)

# Vẽ RSI
st.subheader("Biểu đồ RSI")
fig3, ax3 = plt.subplots(figsize=(12, 3))
ax3.plot(data.index, data['RSI'], label="RSI", color="purple")
ax3.axhline(70, color="red", linestyle="--")
ax3.axhline(30, color="green", linestyle="--")
ax3.set_title(f"{symbol} - RSI")
ax3.legend()
st.pyplot(fig3)

# === Kết luận + Gợi ý MUA/BÁN ===
st.subheader("🔑 Kết Luận & Gợi Ý")

latest = data.tail(1)
price = latest['Close'].values[0].item()
ma20 = latest['MA20'].values[0].item()
rsi = latest['RSI'].values[0].item()
macd_val = latest['MACD'].values[0].item()
macd_sig = latest['MACD_Signal'].values[0].item()

trend = "Giá trên MA20 ➜ Xu hướng TĂNG" if price > ma20 else "Giá dưới MA20 ➜ Xu hướng GIẢM"
rsi_state = (
    "RSI cao ➜ Quá mua" if rsi > 70 else
    "RSI thấp ➜ Quá bán" if rsi < 30 else
    "RSI trung tính"
)
macd_state = (
    "MACD trên Signal ➜ Tín hiệu TĂNG" if macd_val > macd_sig else
    "MACD dưới Signal ➜ Tín hiệu GIẢM"
)

advice = (
    "👉 GỢI Ý: MUA (Uptrend mới bắt đầu)" if (price > ma20 and macd_val > macd_sig and 40 < rsi < 60)
    else "👉 GỢI Ý: BÁN hoặc ĐỨNG NGOÀI (Downtrend)" if (price < ma20 and macd_val < macd_sig)
    else "👉 GỢI Ý: Quan sát thêm, chưa rõ ràng."
)

st.write(f"- **{trend}**")
st.write(f"- **{rsi_state}**")
st.write(f"- **{macd_state}**")
st.info(advice)
