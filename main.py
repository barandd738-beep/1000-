import os
import re
import time
import requests
from playwright.sync_api import sync_playwright

URL = "https://thesakultah23.com/points-market"
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def telegram(mesaj):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": mesaj},
        timeout=20
    ).raise_for_status()

def stok_kontrol(page):
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(8000)

    text = page.locator("body").inner_text()
    text = re.sub(r"\s+", " ", text)

    urun = "1000 TL Nakit (Ref Özel)"
    konum = text.find(urun)

    if konum == -1:
        print("Ürün bulunamadı.")
        return None

    bolum = text[konum:konum + 350]

    eslesme = re.search(
        r"Stok\s*Adedi\s*:\s*(\d+)\s*/\s*10",
        bolum,
        re.IGNORECASE
    )

    if not eslesme:
        print("Stok bilgisi okunamadı.")
        return None

    return int(eslesme.group(1))

def main():
    bildirildi = False

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        telegram("🟢 1000 TL stok takip sistemi başlatıldı!")

        while True:
            try:
                stok = stok_kontrol(page)
                print("Mevcut stok:", stok)

                if stok is not None and stok > 0 and not bildirildi:
                    telegram(
                        f"🚨 1000 TL NAKİT STOKTA!\n"
                        f"Mevcut stok: {stok}/10\n"
                        f"Siteyi hemen kontrol et:\n{URL}"
                    )
                    bildirildi = True

                if stok == 0:
                    bildirildi = False

            except Exception as hata:
                print("Hata:", hata)

            time.sleep(90)

        browser.close()

if __name__ == "__main__":
    main()
