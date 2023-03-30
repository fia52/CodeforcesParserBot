import psycopg2
import time

from codeforces_parser import all_pages_parser
from config import PAGE_URL, HEADERS


class BotBD:
    def __init__(self, host, user, password, db_name):
        try:
            self.connection = psycopg2.connect(
                host=host, user=user, password=password, database=db_name
            )
            self.cursor = self.connection.cursor()

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)

        self.except_str = "'AA'"

    def get_list_of_problems(self, topic: str, complexity: str) -> list:
        """Делает запрос к бд, выдаёт 10 задач по казанной теме и сложности, номера выведенных задач
        сохраняются в переменную атрибут класса, что обеспечивает смену задач по одному и тому же запросу.
        """

        self.cursor.execute(
            f"""SELECT * FROM problems WHERE topic LIKE '%{topic}%' and complexity = '{complexity}' 
                and number not in ({self.except_str}) LIMIT 10"""
        )

        problems = self.cursor.fetchall()
        for problem in problems:
            self.except_str += f", '{problem[0]}'"

        if not problems:
            self.except_str = "'AA'"
            self.get_list_of_problems(topic, complexity)

        if len(problems) < 10:
            self.except_str = "'AA'"

        return problems

    def add_list_of_records(self, list_of_records: list[dict]) -> None:
        """Добавляет список записей в таблицу"""
        list_of_values = list(map(lambda x: list(x.values()), list_of_records))

        self.cursor.executemany(
            """INSERT INTO problems (number, name, topic, complexity, solutions_num)
            VALUES (%s, %s, %s, %s, %s)""",
            list_of_values,
        )

        self.connection.commit()

    def drop_table(self) -> None:
        """Удаляет все записи из таблицы"""
        self.cursor.execute("""DELETE FROM problems""")
        self.connection.commit()

    def autoupdater(self) -> None:
        """Полностью обновляет таблицу раз в час (примерно за 50 секунд)"""

        while True:
            list_of_records = all_pages_parser(PAGE_URL, HEADERS)
            self.drop_table()
            self.add_list_of_records(list_of_records)
            print("[INFO] BD has just updated!")
            time.sleep(60 * 60)

    async def close(self) -> None:
        """Закрываем соединение с БД"""
        self.cursor.close()
        self.connection.close()
