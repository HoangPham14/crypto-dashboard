import yfinance as yf
import pandas as pd
import ta
import smtplib
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def analyze_and_send():
    # === Phân tích BTC ===
    symbol = "BTC-USD"
    data = yf.download(symbol, start="2023-01-01")

    if data.empty:
        print("❌ Không có dữ liệu BTC, thử lại sau.")
        return

    close = data['Close'].squeeze()
    data['MA20'] = close.rolling(window=20).mean()
    data['RSI'] = ta.momentum.RSIIndicator(close, window=14).rsi()
    macd = ta.trend.MACD(close)
    data['MACD'] = macd.macd()
    data['MACD_Signal'] = macd.macd_signal()

    latest = data.tail(1)
    price = latest['Close'].values[0].item()
    ma20 = latest['MA20'].values[0].item()
    rsi = latest['RSI'].values[0].item()
    macd_val = latest['MACD'].values[0].item()
    macd_sig = latest['MACD_Signal'].values[0].item()

    if price > ma20:
        trend = "Giá trên MA20 ➜ Xu hướng TĂNG"
    else:
        trend = "Giá dưới MA20 ➜ Xu hướng GIẢM"

    if rsi > 70:
        rsi_state = "RSI cao ➜ Quá mua"
    elif rsi < 30:
        rsi_state = "RSI thấp ➜ Quá bán"
    else:
        rsi_state = "RSI trung tính"

    if macd_val > macd_sig:
        macd_state = "MACD trên Signal ➜ Tín hiệu TĂNG"
    else:
        macd_state = "MACD dưới Signal ➜ Tín hiệu GIẢM"

    # Gợi ý điểm mua/bán
    if (price > ma20) and (macd_val > macd_sig) and (40 < rsi < 60):
        advice = "👉 GỢI Ý: Tín hiệu MUA hợp lý."
    elif (price < ma20) and (macd_val < macd_sig):
        advice = "👉 GỢI Ý: Tín hiệu BÁN hoặc đứng ngoài."
    else:
        advice = "👉 GỢI Ý: Thị trường chưa rõ, nên quan sát thêm."

    # Nội dung email
    text = f"""
=== Báo Cáo BTC Hôm Nay ===
Giá hiện tại: {price:.2f} USD
MA20: {ma20:.2f} USD
RSI: {rsi:.2f}
MACD: {macd_val:.2f}
MACD Signal: {macd_sig:.2f}

{trend}
{rsi_state}
{macd_state}

{advice}
    """

    # === GỬI EMAIL ===
    sender_email = "hoangpm14@gmail.com"
    receiver_email = "hoangpm14@gmail.com"
    password = "fbbr awbo attw yyf"

    message = MIMEMultipart("alternative")
    message["Subject"] = "⏰ Báo Cáo BTC Hằng Ngày"
    message["From"] = sender_email
    message["To"] = receiver_email
    part = MIMEText(text, "plain")
    message.attach(part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("✅ Đã gửi email thành công!")
    except Exception as e:
        print("❌ Lỗi khi gửi email:", e)

# === Lịch chạy: mỗi ngày 8:00 sáng ===
schedule.every().day.at("08:00").do(analyze_and_send)

print("🌿 Bot báo cáo BTC đã sẵn sàng. Đang chờ lịch chạy...")

while True:
    schedule.run_pending()
    time.sleep(60)
