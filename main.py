import os
import re
import requests

URL = "https://thesakultah23.com/points-market"
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def telegram(message):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": message},
        timeout=20
    ).raise_for_status()

def main():
    response = requests.get(URL, timeout=30)
    response.raise_for_status()

    text = re.sub(r"\s+", " ", response.text)

    product = "1000 TL Nakit (Ref Özel)"
    if product.lower() not in text.lower():
        print("Ürün sayfada bulunamadı.")
        return

    match = re.search(
        r"Stok\s*Adedi\s*:\s*(\d+)\s*/\s*10",
        text,
        re.IGNORECASE
    )

    if not match:
        print("Stok bilgisi okunamadı.")
        return

    stock = int(match.group(1))
    print(f"Stok: {stock}/10")

    if stock > 0:
        telegram(
            f"🚨 1000 TL NAKİT STOKTA!\n"
            f"Stok: {stock}/10\n{URL}"
        )

if __name__ == "__main__":
    main()
