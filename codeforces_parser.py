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
                "number": problem.find_all("td")[0].text.strip()
                if problem.find_all("td")[0]
                else "None",
                "name": problem.find_all("td")[1].find_all("div")[0].text.strip()
                if problem.find_all("td")[1]
                and problem.find_all("td")[1].find_all("div")[0]
                else "None",
                "topic": ", ".join(
                    map(
                        lambda x: x.text.strip(),
                        problem.find_all("td")[1].find_all("div")[1].find_all("a"),
                    )
                )
                if problem.find_all("td")[1]
                and problem.find_all("td")[1].find_all("div")[1]
                else "None",
                "complexity": problem.find_all("td")[3].text.strip()
                if problem.find_all("td")[3]
                else "None",
                "solutions_num": problem.find_all("td")[4].text.strip()
                if problem.find_all("td")[4]
                else "None",
            }
            list_of_records.append(record)

    return list_of_records
