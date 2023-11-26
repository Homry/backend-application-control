import psycopg2
from psycopg2 import sql


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="1234",
            host="127.0.0.1",
            port="5432",
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

        self.dbname = "status_app_db"
        self.table_name = "status_app"
        if not self.__check_db_exist():
            self.__create_db()
        else:
            print("Схема уже существует")

        if not self.__check_table_exist():
            self.__create_table()
        else:
            print("Таблица уже существует")

    def __check_db_exist(self):
        query = sql.SQL(
            "SELECT EXISTS (SELECT 1 FROM pg_catalog.pg_namespace WHERE nspname = %s)"
        )
        self.cursor.execute(query, (self.dbname,))
        return self.cursor.fetchone()[0]

    def __create_db(self):
        self.cursor.execute(
            sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(self.dbname))
        )
        print(f"Схема '{self.dbname}' создана")

    def __check_table_exist(self):
        query = sql.SQL(
            "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = %s AND \
                        table_name = %s)"
        )
        self.cursor.execute(query, (self.dbname, self.table_name))
        return self.cursor.fetchone()[0]

    def __create_table(self):
        query_create = sql.SQL(
            "CREATE TABLE {}.{} (id serial PRIMARY KEY, time TIME, date DATE, name VARCHAR, \
                               status VARCHAR);"
        ).format(sql.Identifier(self.dbname), sql.Identifier(self.table_name))
        self.cursor.execute(query_create)
        print(f"Таблица '{self.table_name}' создана в схеме '{self.dbname}'")

    def insert_data(self, app_name, status):
        query_insert = sql.SQL(
            "INSERT INTO {}.{} (time, date, name, status) VALUES (CURRENT_TIME, CURRENT_DATE, \
                                %s, %s);"
        ).format(sql.Identifier(self.dbname), sql.Identifier(self.table_name))
        self.cursor.execute(query_insert, (app_name, status))
        print(f"Данные для приложения '{app_name}' успешно добавлены")

    def get_data_with_pagination(self, page_size=10, page_number=1):
        offset = (page_number - 1) * page_size

        query = sql.SQL("SELECT * FROM {}.{} LIMIT %s OFFSET %s").format(
            sql.Identifier(self.dbname), sql.Identifier(self.table_name)
        )

        self.cursor.execute(query, (page_size, offset))
        rows = self.cursor.fetchall()
        return rows

    def get_data_all(self):
        query = sql.SQL("SELECT * FROM {}.{}").format(
            sql.Identifier(self.dbname), sql.Identifier(self.table_name)
        )

        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows


if __name__ == "__main__":
    db = Database()
    db.insert_data("excel", "Running")
    print(db.get_data_all())
