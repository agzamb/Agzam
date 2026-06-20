import telebot
import requests
import time

# Sizning ma'lumotlaringiz
BOT_TOKEN = '8623542413:AAHv34JV1FIyTJLC4YIj7B_rTi9ULoQnd40'
CHANNEL_ID = '@solanapriceuzs'

bot = telebot.TeleBot(BOT_TOKEN)

def get_fiat_rates():
    try:
        # Valyuta kurslarini olish API-si
        resp = requests.get("https://api.exchangerate-api.com/v4/latest/USD").json()
        usd_to_uzs = float(resp['rates']['UZS'])
        usd_to_kzt = float(resp['rates']['KZT'])
        usd_to_rub = float(resp['rates']['RUB'])
        
        # Tenge va Rublning so'mdagi qiymatini hisoblash
        kzt_to_uzs = round(usd_to_uzs / usd_to_kzt, 2)
        rub_to_uzs = round(usd_to_uzs / usd_to_rub, 2)
        
        return usd_to_uzs, kzt_to_uzs, rub_to_uzs
    except Exception:
        # Xatolik bo'lsa, taxminiy joriy kurslar
        return 12850.0, 28.5, 145.0

def get_crypto_prices():
    try:
        # Valyuta kurslarini yangilash
        usd_rate, kzt_rate, rub_rate = get_fiat_rates()

        # Binance API-dan SOL, TON va BTC narxlarini olish
        sol_resp = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT").json()
        ton_resp = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=TONUSDT").json()
        btc_resp = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()
        
        # CoinGecko API-dan GRAM narxini olish
        gram_resp = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=gram&vs_currencies=usd").json()
        
        # Dollardagi narxlar
        sol_usd = float(sol_resp['price'])
        ton_usd = float(ton_resp['price'])
        btc_usd = float(btc_resp['price'])
        gram_usd = gram_resp.get('gram', {}).get('usd', 0.007)
        
        # So'mdagi narxlar
        sol_uzs = round(sol_usd * usd_rate)
        gram_uzs = round(gram_usd * usd_rate, 2)
        ton_uzs = round(ton_usd * usd_rate)
        btc_uzs = round(btc_usd * usd_rate)
        
        # Xabar matni
        text = (
            f"SOL - ${sol_usd:,.2f} ({sol_uzs:,} so'm)\n"
            f"GRAM - ${gram_usd} ({gram_uzs:,} so'm)\n"
            f"TON - ${ton_usd:,.2f} ({ton_uzs:,} so'm)\n"
            f"BTC - ${btc_usd:,.0f} ({btc_uzs:,} so'm)\n"
            f"-------------------------\n"
            f"💵 1 USD = {usd_rate:,} so'm\n"
            f"🇰🇿 1 KZT = {kzt_rate} so'm\n"
            f"🇷🇺 1 RUB = {rub_rate} so'm"
        )
        return text
    except Exception as e:
        print(f"Narxni olishda xatolik: {e}")
        return None

print("Bot barcha valyutalar (USD, KZT, RUB) bilan ishga tushdi...")

while True:
    matn = get_crypto_prices()
    
    if matn:
        try:
            bot.send_message(CHANNEL_ID, matn)
            print("Kurslar to'liq holda kanalga yuborildi!")
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")
            
    # 1 daqiqa kutish
    time.sleep(60)
  
