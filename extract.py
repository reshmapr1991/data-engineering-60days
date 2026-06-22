import requests
from bs4 import BeautifulSoup
url = "https://www.napacanada.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text,"html.parser")
#print(soup.prettify())
soup.find_all("div",class_ = "accountlay")
print(soup.prettify())
soup.find_all("div",class_ = "a")



# Display extracted quotes
