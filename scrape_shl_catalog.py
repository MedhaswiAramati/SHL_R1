import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.shl.com/solutions/products/product-catalog/"
headers = {
    "User-Agent": "Mozilla/5.0"
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# Update this based on SHL's actual page structure
cards = soup.find_all("div", class_="col-sm-6 col-md-4 col-lg-3 mb-4 product-card")

data = []
for card in cards:
    title_tag = card.find("h3")
    desc_tag = card.find("div", class_="product-description")
    link_tag = card.find("a", href=True)

    if title_tag and desc_tag and link_tag:
        name = title_tag.text.strip()
        description = desc_tag.text.strip()
        link = "https://www.shl.com" + link_tag['href']
        data.append({
            "name": name,
            "url": link,
            "remote": "Yes",  # hardcoded unless you want to detect this
            "description": description
        })

df = pd.DataFrame(data)
df.to_csv("data/assessments.csv", index=False)
print(f"✅ Scraped {len(data)} assessments and saved to assessments.csv")
