from json import dump
from requests import get
from bs4 import BeautifulSoup

BASE_URL = "https://www.uzhnu.edu.ua"
page = get(f"{BASE_URL}/uk/cat/faculty")

uzhnu = []

soup = BeautifulSoup(page.content, "html.parser")
fac_list = soup.find("ul", class_="departments_unfolded")
for li in fac_list.findChildren("li"):
    a = li.find("a")
    fac_name = a.find(text=True, recursive=False)
    faculty = {
        "name":fac_name,
        "departments":[]
    }
    ref = a.get("href")
    if ref:
        dep_page = get(f"{BASE_URL}{ref}")
        dep_soup = BeautifulSoup(dep_page.content, "html.parser")
        dep_list = dep_soup.find(class_="departments")
        for li in dep_list.find_all("li"):
            a = li.find("a")
            dep_name = a.find(text=True, recursive=False)
            department = {
                "name": dep_name,
                "scientists":[]
            }
            faculty["departments"].append(department)
    uzhnu.append(faculty)

with open("res.json", "w", encoding="utf-8") as file:
    dump(uzhnu, file, ensure_ascii=False, indent=4)