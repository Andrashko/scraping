from json import dump
from requests import get
from bs4 import BeautifulSoup
import re
from sqlite3 import connect

BASE_URL = "https://www.uzhnu.edu.ua"
URL = f"{BASE_URL}/uk/cat/faculty"
NAME_PATTERNS = [
    r"[А-ЯІЇЄ]{1}[а-яіїє]+\s+[А-ЯІЇЄ]{1}[а-яіїє]+\s+[А-ЯІЇЄ]{1}[а-яіїє]+",
    r"[А-ЯІЇЄ]{1}[а-яіїє]+\s+[А-ЯІЇЄ]{1}\.\s*[А-ЯІЇЄ]{1}\.",
]


page = get(URL)
soup = BeautifulSoup(page.content,  "html.parser")

faculties = []

#робота з базою даних
connection = connect("uzhnu.db")
cursor = connection.cursor()

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

        for f in cursor.execute(
            "SELECT id FROM faculties WHERE name=?",
            [faculty["name"]]
        ):
            faculty["id"] = f[0]
        
        if not faculty.get("id"):
            cursor.execute(
                "INSERT INTO faculties (name, url) VALUES (?,?)",
                [faculty["name"], faculty["url"]]
            )
            connection.commit()
            for f in cursor.execute(
                "SELECT id FROM faculties WHERE name=?",
                [faculty["name"]]
            ):
                faculty["id"] = f[0]




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
            
            for d in cursor.execute(
                "SELECT id FROM departments WHERE name=?",
                [department["name"]]
            ):
                department["id"] = d[0]
        
            if not department.get("id"):
                cursor.execute(
                    "INSERT INTO departments (name, url, faculty_id) VALUES (?,?,?)",
                    [department["name"], department["url"], faculty["id"]]
                )
                connection.commit()
                for d in cursor.execute(
                    "SELECT id FROM departments WHERE name=?",
                    [department["name"]]
                ):
                    department["id"] = d[0]


            staff_page = get(f"{dep_link}/staff")
            staff_soup = BeautifulSoup(staff_page.content,"html.parser")
            for staff_list in staff_soup.find_all("ol"):
                for staff_li in staff_list.find_all("li"):
                    staff = ""
                    staff_text = staff_li.find(text=True, recursive=False)
                    if not staff_text:
                        span = staff_li.find("span")
                        staff_text = span.find(text=True, recursive=False)
                    # тут ще потрібні інші костилі для деяких сторінок
                    if not staff_text:
                        continue
                    for pattern in NAME_PATTERNS:
                        res = re.search( pattern, staff_text)
                        if res:
                            staff = res.group(0)
                            break
                    if staff:
                        department["staff"].append(staff)
                        print(staff)

            faculty["departments"].append(department)
        faculties.append(faculty)

   


with open("uzhnu.json", "w", encoding="utf-8") as json_file:
    dump(faculties, json_file, ensure_ascii=False, indent=4)        