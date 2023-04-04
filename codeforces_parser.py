import bs4.element
import requests
from bs4 import BeautifulSoup


def get_cur_num_of_pages(url: str, headers: dict) -> int:
    """Узнаём количество страниц сайта на данный момент."""

    request = requests.get(url, headers)
    src = request.text
    soup = BeautifulSoup(src, "lxml")

    list_of_nums = soup.find_all("span", class_="page-index")

    num_of_pages = list(map(lambda x: int(x.text), list_of_nums))[-1]

    return num_of_pages


def all_pages_parser(url: str, headers: dict) -> list[dict]:
    """Перебираем все страницы, парсим инфу о задачах."""

    num_of_pages = get_cur_num_of_pages(url.format(page_num=1), headers)

    list_of_records = []

    for i in range(1, num_of_pages + 1):
        page_url = url.format(page_num=i)
        request = requests.get(page_url, headers)
        src = request.text
        soup = BeautifulSoup(src, "lxml")

        problems = soup.find("table", class_="problems").find_all("tr")[1:]

        for problem in problems:
            record = {
                "number": get_text_by_path(problem, "1.a"),
                "name": get_text_by_path(problem, "3.1.a"),
                "topic": " ".join(map(lambda x: x.strip(), get_text_by_path(problem, "3.3").split('\n'))),
                "complexity": get_text_by_path(problem, "7.span"),
                "solutions_num": get_text_by_path(problem, "9.a")
            }
            list_of_records.append(record)

    return list_of_records


def get_text_by_path(element: bs4.element.Tag, path: str) -> str:
    """
    Получаем путь к искомому элементу в виде td.1.div.0.a и отдаем его
    """

    keys = path.split(".")
    result = element

    for key in keys:
        try:
            if key.isdigit():
                result = result.contents[int(key)]
            else:
                result = result.find(key)

            if not result:
                return "None"

        except (AttributeError, IndexError):
            return "None"

    return result.text.strip()
