from requests import get
from bs4 import BeautifulSoup
URL = f"https://webcache.googleusercontent.com/search?q=cache:gufH1CE5SLwJ:https://www.univer.kharkov.ua/ua/departments/sociology/sociology_staff+&cd=2&hl=ru&ct=clnk&gl=ua"
page = get(URL)
soup = BeautifulSoup(page.content,  "html.parser")
print (soup.prettify())