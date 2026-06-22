import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.amazon.in/Yoga-Bar-Protein-Chocolate-Chips/dp/B0DG1XFJ1Q/ref=sr_1_27?crid=3136MS0EWZOJ4&dib=eyJ2IjoiMSJ9.UjRbHVUnzwjyZ1re7TeP0iyOmh152lAUuVqQNe8CyRNNfECI83PN1pIA6oSSRAWOynl6T0gDoVBoajfwPTJUpSiuU6zwZe14-bKYZo7adQj99_OyGbtLmx7ZfzrEU2buJSMog--_HVBJJ51S-MHQ05Us9dXlPnTIUpK2iEGqTgQk2a67p-T_Clt5QpLn8S654PgFzm0Om_LGTEdB2JsximVTz1eGlL-wdWGF61UmL0kSen9x4HLJwyyiwHnkSJfxC31aDZPv_6ILWIdw5XfgKtCo0XoVNApZ1uZ7rovXKis.RLXqL2DU60KfdAI496PMb0wFpoClKvLyL_xgzgXp4j4&dib_tag=se&keywords=protein+bar+YOGA+BAR&qid=1763913534&sprefix=protein+bar+yoga+bar%2Caps%2C226&sr=8-27")



html = driver.page_source
soup = BeautifulSoup(html, "html.parser")



title = soup.select_one("#productTitle")
image = soup.select_one("img")
rating = soup.select_one("i").get_text(strip=True)
count = soup.select_one("#arcCustomerReviewText")

print(title, image, rating, count)



# Step 3: Create a dictionary or DataFrame
data = {
    "Title": [title],
    "Image URL": [image],
    "Rating": [rating],
    "Review Count": [count]
}

df = pd.DataFrame(data)

# Step 4: Write to Excel
df.to_excel("amazon_product.xlsx", index=True)
