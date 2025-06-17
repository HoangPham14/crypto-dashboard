import yfinance as yf
import pandas as pd
import ta
import matplotlib.pyplot as plt

# Tải dữ liệu BTC
symbol = "BTC-USD"
data = yf.download(symbol, start="2023-01-01")

if data.empty:
    print("Không có dữ liệu BTC, hãy thử lại.")
    exit()

# Ép cột Close thành Series
close = data['Close'].squeeze()

# Tính chỉ báo
data['MA20'] = close.rolling(window=20).mean()
data['RSI'] = ta.momentum.RSIIndicator(close, window=14).rsi()
macd = ta.trend.MACD(close)
data['MACD'] = macd.macd()
data['MACD_Signal'] = macd.macd_signal()

# In dữ liệu mới nhất
latest = data.tail(1)

# Dùng .item() để lấy giá trị chuẩn
price = latest['Close'].values[0].item()
ma20 = latest['MA20'].values[0].item()
rsi = latest['RSI'].values[0].item()
macd_val = latest['MACD'].values[0].item()
macd_sig = latest['MACD_Signal'].values[0].item()

print("\n=== Phân tích BTC ===")
print(f"Giá hiện tại: {price:.2f} USD")
print(f"MA20: {ma20:.2f} USD")
print(f"RSI: {rsi:.2f}")
print(f"MACD: {macd_val:.2f}")
print(f"MACD Signal: {macd_sig:.2f}")
print("\n=== Gợi ý điểm mua/bán (mang tính tham khảo) ===")

# Kết luận xu hướng đơn giản
if latest['Close'].values[0] > latest['MA20'].values[0]:
    trend = "Giá đang ở TRÊN MA20 ➜ Xu hướng NGẮN HẠN là TĂNG"
else:
    trend = "Giá đang ở DƯỚI MA20 ➜ Xu hướng NGẮN HẠN là GIẢM"

if latest['RSI'].values[0] > 70:
    rsi_state = "RSI cao ➜ Thị trường có thể QUÁ MUA"
elif latest['RSI'].values[0] < 30:
    rsi_state = "RSI thấp ➜ Thị trường có thể QUÁ BÁN"
else:
    rsi_state = "RSI trung tính ➜ Không quá mua/bán rõ rệt"

if latest['MACD'].values[0] > latest['MACD_Signal'].values[0]:
    macd_state = "MACD cắt lên Signal ➜ Tín hiệu TĂNG"
else:
    macd_state = "MACD dưới Signal ➜ Tín hiệu GIẢM hoặc YẾU"

print(f"\n>>> {trend}")
print(f">>> {rsi_state}")
print(f">>> {macd_state}")

# === GỢI Ý ĐIỂM MUA/BÁN ===
print("\n=== Gợi ý điểm mua/bán (mang tính tham khảo) ===")

if (price > ma20) and (macd_val > macd_sig) and (40 < rsi < 60):
    print("👉 GỢI Ý: Tín hiệu MUA hợp lý (Uptrend mới bắt đầu).")
elif (price < ma20) and (macd_val < macd_sig):
    print("👉 GỢI Ý: Tín hiệu BÁN hoặc đứng ngoài (Downtrend).")
else:
    print("👉 GỢI Ý: Thị trường chưa rõ ràng, nên quan sát thêm hoặc đặt stop-loss cẩn thận.")

# Vẽ biểu đồ
plt.figure(figsize=(14, 7))
plt.plot(close, label='Close Price')
plt.plot(data['MA20'], label='MA 20')
plt.title(f'{symbol} - Xu hướng hiện tại')
plt.legend()
plt.show()
