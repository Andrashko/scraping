from json import dump
from requests import get
from bs4 import BeautifulSoup

BASE_URL = "https://www.uzhnu.edu.ua"
URL = f"{BASE_URL}/uk/cat/faculty"
page = get(URL)
soup = BeautifulSoup(page.content,  "html.parser")

faculties = []

with open("uzhnu.txt", "w", encoding="utf-8") as file:
    fac_list = soup.find(class_="departments_unfolded")
    for li in fac_list.find_all("li"):
        
        a = li.find("a")
        fac_name = a.find(text=True, recursive=False)
        file.write(f"{fac_name}\n")
        link = BASE_URL+ a.get("href")
        faculty = {
            "name": fac_name,
            "url": link,
            "departments": []
        }

        fac_page = get(link)
        fac_soup = BeautifulSoup(fac_page.content, "html.parser")
        dep_list = fac_soup.find(class_="departments")
        for dep_li in dep_list.find_all("li"):
            a = dep_li.find("a")
            dep_name = a.find(text=True, recursive=False)
            file.write(f"   {dep_name}\n")
            dep_link = BASE_URL+a.get('href')
            department = {
                "name": dep_name,
                "url": dep_link,
                "staff": [] 
            }
            
            staff_page = get(f"{dep_link}/staff")
            staff_soup = BeautifulSoup(staff_page.content,"html.parser")
            for staff_list in staff_soup.find_all("ol"):
                for staff_li in staff_list.find_all("li"):
                    staff_text = staff_li.find(text=True, recursive=False)
                    if not staff_text:
                        span = staff_li.find("span")
                        staff_text = staff_li.find(text=True, recursive=False)
                    department["staff"].append(staff_text)
                    print(staff_text)

            faculty["departments"].append(department)
        faculties.append(faculty)

with open("uzhnu.json", "w", encoding="utf-8") as json_file:
    dump(faculties, json_file, ensure_ascii=False, indent=4)        