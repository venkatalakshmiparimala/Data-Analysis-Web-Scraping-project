from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

# ---------- Setup Chrome options ----------
options = Options()
# options.add_argument("--headless")  # Uncomment to run headless
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(r"D:\projects\GTAGRA project\Assignment-2\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# ---------- Open URL ----------
url = "https://journals.sagepub.com/toc/jmx/current"
driver.get(url)
time.sleep(5)

# ---------- Accept cookies ----------
try:
    accept_btn = driver.find_element(By.XPATH, "//button[contains(., 'Accept Non-Essential Cookies')]")
    accept_btn.click()
    print("[DEBUG] Accepted cookies")
    time.sleep(2)
except:
    print("[DEBUG] Cookie banner not found or already dismissed")

# ---------- Parse TOC page ----------
soup = BeautifulSoup(driver.page_source, "html.parser")
articles = soup.select("div.issue-item")

print(f"[DEBUG] {len(articles)} articles found")

data = []

# ---------- Loop through articles ----------
for i, article in enumerate(articles):
    print(f"[DEBUG] Parsing article {i+1}")

    # Title
    title_tag = article.select_one("h5.issue-item__heading")
    title = title_tag.text.strip() if title_tag else "N/A"

    # Authors
    authors_tags = article.select("div.issue-item__authors ul li span")
    authors = [a.text.strip() for a in authors_tags]
    authors_str = "; ".join(authors) if authors else "N/A"

    # Abstract
    abstract_tag = article.select_one("div.issue-item__abstract__content")
    if abstract_tag:
        abstract_text = abstract_tag.get_text(separator=" ", strip=True)
        abstract_text = abstract_text.replace("Abstract", "").strip()
    else:
        abstract_text = "N/A"

    # First published date
    pub_header = article.select_one("div.issue-item__header")
    pub_date = "N/A"
    if pub_header:
        spans = pub_header.find_all("span")
        for s in spans:
            if "First published" in s.text:
                pub_date = s.text.strip()
                break

    # DOI (from href)
    doi_tag = article.select_one("div.issue-item__title a")
    doi = "N/A"
    if doi_tag and "href" in doi_tag.attrs:
        doi = "https://doi.org" + doi_tag['href'].replace("/doi/abs", "")

    # Debug print
    print(f"Title: {title}")
    print(f"Authors: {authors_str}")
    print(f"Date: {pub_date}")
    print(f"DOI: {doi}")
    print(f"Abstract: {abstract_text[:60]}...")
    print("-" * 80)

    data.append({
        "Title": title,
        "Authors": authors_str,
        "First Published Date": pub_date,
        "DOI": doi,
        "Abstract": abstract_text
    })

# ---------- Save to CSV ----------
output_path = "D:/projects/GTAGRA project/Assignment-2/assignment2_articles_final.csv"
df = pd.DataFrame(data)
df.to_csv(output_path, index=False, encoding="utf-8-sig")
print(f"\n✅ Scraping complete. CSV saved at: {output_path}")

driver.quit()
