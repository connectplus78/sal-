import json
import os
import cloudscraper
from bs4 import BeautifulSoup

# Hedef kategori URL'si
TARGET_URL = "https://www.hdfilmcehennemi.now/top-rated/"

def scrape_movies():
    # Cloudflare korumalarını aşmak için cloudscraper kullanıyoruz
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )

    try:
        print(f"Bağlanılıyor: {TARGET_URL}")
        response = scraper.get(TARGET_URL, timeout=20)
        
        if response.status_code != 200:
            print(f"Bağlantı hatası, HTTP Kod: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        movies = []

        # Sitenin güncel film kartı seçicileri
        item_elements = soup.select(".poster-container, .film-box, .card, .item")

        for item in item_elements:
            title_elem = item.select_one(".title, h3, .film-title, .name")
            link_elem = item.select_one("a")
            img_elem = item.select_one("img")

            title = title_elem.get_text(strip=True) if title_elem else "İsimsiz"
            url = link_elem['href'] if link_elem and link_elem.has_attr('href') else ""
            
            # Görsel adresini güvenli bir şekilde al
            poster = ""
            if img_elem:
                for attr in ['data-src', 'src', 'data-original']:
                    if img_elem.has_attr(attr):
                        poster = img_elem[attr]
                        break

            # Göreceli linkleri tam adrese çevir
            if url and not url.startswith('http'):
                url = "https://www.hdfilmcehennemi.now" + url

            if url:
                movies.append({
                    "title": title,
                    "url": url,
                    "poster": poster
                })

        return movies
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return []

if __name__ == "__main__":
    data = scrape_movies()
    print(f"Bulunan içerik sayısı: {len(data)}")
    
    # Görseldeki dosya adıyla uyumlu olması için 'filmler.json' olarak kaydediyoruz
    with open("filmler.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print("Veriler filmler.json dosyasına başarıyla yazıldı.")
