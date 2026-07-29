import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def scrape_with_selenium():
  # Tarayıcıyı gizli ve otomatik modda başlatıyoruz (Cloudflare'i geçmek için en etkili yöntem)
  options = Options()
  # options.add_argument("--headless") # Tarayıcının ekranda açılmasını istemiyorsan bu satırdaki # işaretini kaldırabilirsin
  options.add_argument("--disable-gpu")
  options.add_argument("--no-sandbox")
  options.add_argument(
      "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
  )

  driver = webdriver.Chrome(options=options)
  target_url = "https://www.hdfilmcehennemi.now/top-rated/"

  print(f"Siteye bağlanılıyor: {target_url}")
  driver.get(target_url)

  # Cloudflare doğrulamasının veya sayfa yüklenmesinin tamamlanması için birkaç saniye bekliyoruz
  time.sleep(5)

  soup = BeautifulSoup(driver.page_source, "html.parser")
  driver.quit()

  movies = []
  # Sitenin güncel HTML yapılarına ait olası tüm seçiciler
  item_elements = soup.select(
      ".poster-container, .film-box, .card, .item, .tray-item"
  )
  print(f"Bulunan element sayısı: {len(item_elements)}")

  for item in item_elements:
    title_elem = item.select_one(".title, h3, .film-title, .name")
    link_elem = item.select_one("a")
    img_elem = item.select_one("img")

    title = title_elem.get_text(strip=True) if title_elem else "İsimsiz"
    url = link_elem["href"] if link_elem and link_elem.has_attr("href") else ""

    poster = ""
    if img_elem:
      for attr in ["data-src", "src", "data-original", "srcset"]:
        if img_elem.has_attr(attr):
          poster = img_elem[attr]
          break

    if url and not url.startswith("http"):
      url = "https://www.hdfilmcehennemi.now" + url

    if url:
      movies.append({"title": title, "url": url, "poster": poster})

  return movies


if __name__ == "__main__":
  data = scrape_with_selenium()

  # Sonucu filmler.json olarak kaydediyoruz
  with open("filmler.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

  print(f"İşlem tamam! Toplam {len(data)} film filmler.json dosyasına yazıldı.")
