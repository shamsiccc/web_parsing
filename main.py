import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json

def get_headers():
    return Headers(browser="chrome", os="win").generate()

def get_vacancies():
    main_response = requests.get("https://hh.ru/vacancy/", headers=get_headers())
    main_html = main_response.text
    main_soup = BeautifulSoup(main_html, "lxml")

    vacancies_list = main_soup.find_all("div", class_="vacancy-serp-item")

    parsed_data = []

    for vacancy in vacancies_list:
        link_tag = vacancy.find("main", class_="vacancy-serp-content")
        link = link_tag["href"] if link_tag else "Нет ссылки"

        salary_tag = vacancy.find("span",
                                  class_="magritte-text___pbpft_3-0-15 magritte-text_style-primary___AQ7MW_3-0-15 magritte-text_typography-label-1-regular___pi3R-_3-0-15")
        salary = salary_tag.text.strip() if salary_tag else "Не указана"

        description_tag = vacancy.find("div", class_="g-user-content")
        description = description_tag.text.strip() if description_tag else ""

        if "Django" in description and "Flask" in description:
            parsed_data.append({
                "link": link,
                "salary": salary,
            })

    return parsed_data

vacancies = get_vacancies()

with open("vacancies.json", "w", encoding="utf-8") as f:
    json.dump(vacancies, f, ensure_ascii=False, indent=2)

print(f"Найдено {len(vacancies)} вакансий.")