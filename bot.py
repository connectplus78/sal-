import json
import os
from bs4 import BeautifulSoup
import requests

# Örnek hedef kategori URL'si (Kendi yapılandırmanıza göre düzenleyebilirsiniz)
TARGET_URL = "https://www.hdfilmcehennemi.now/top-rated/"  # veya benzeri kategori


def scrape_movies():
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/120.0.0.0 Safari/537.36"
      )
  }

  try:
    response = requests.get(TARGET_URL, headers=headers, timeout=15)
    if response.status_code != 200:
      print(f"Bağlantı hatası: {response.status_code}")
      return []

    soup = BeautifulSoup(response.text, "html.parser")
    movies = []

    # Sitenin güncel HTML yapısına göre kart seçicileri (Örnek yapı)
    item_elements = soup.select(".poster-container, .film-box, .card")

    for item in item_elements:
      title_elem = item.select_one(".title, h3, .film-title")
      link_elem = item.select_one("a")
      img_elem = item.select_one("img")

      title = title_elem.get_text(strip=True) if title_elem else "İsimsiz"
      url = link_elem["href"] if link_elem and link_elem.has_attr("href") else ""
      poster = (
          img_elem["data-src"]
          if img_elem and img_elem.has_attr("data-src")
          else (img_elem["src"] if img_elem and img_elem.has_attr("src") else "")
      )

      if url:
        movies.append({"title": title, "url": url, "poster": poster})

    return movies
  except Exception as e:
    print(f"Hata oluştu: {e}")
    return []


if __name__ == "__main__":
  data = scrape_movies()
  # GitHub Pages üzerinde okunacak JSON dosyası
  with open("movies.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
  print(f"Toplam {len(data)} içerik başarıyla kaydedildi.")
