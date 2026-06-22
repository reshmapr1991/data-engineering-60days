
from bs4 import BeautifulSoup
import requests

url ="https://www.amazon.in/s?bbn=81107432031&rh=n%3A81107432031%2Cp_85%3A10440599031&_encoding=UTF8&content-id=amzn1.sym.58c90a12-100b-4a2f-8e15-7c06f1abe2be&pd_rd_r=df8f4fa9-2d64-4c50-84d3-ef91771d8e7a&pd_rd_w=XhVlZ&pd_rd_wg=5q4pY&pf_rd_p=58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_r=7DHWP2V80Y2M700QZ3ZV&ref=pd_hp_d_atf_unk"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-IN,en;q=0.9"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")


items = soup.select("div.s-main-slot div.s-result-item")

for item in items:
    asin = item.get("data-asin")
    title = item.select_one("h2 a span")
    rating = item.select_one("span.a-icon-alt")
    price = item.select_one("span.a-price-whole")

    if title:
        print("ASIN:", asin)
        print("Title:", title.text.strip())
        print("Rating:", rating.text if rating else None)
        print("Price:", price.text if price else None)
        print("URL:", "https://www.amazon.in/dp/" + asin)
        print("----")
