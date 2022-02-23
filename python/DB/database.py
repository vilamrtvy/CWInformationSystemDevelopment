# Сторонние пакеты
from pymysql import connect
from pymysql import OperationalError


class DBConnect:
    def __init__(self, config: dict):
        self.config = config
        self.conn = None

    def __enter__(self):
        try:
            self.conn = connect(**self.config)
            self.cursor = self.conn.cursor()

            return self.cursor
        except OperationalError as err:
            if err.args[0] == 1049:
                print('1')
            elif err.args[0] == 1045:
                print('2')
            elif err.args[0] == 2003:
                print('3')
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            if exc_val.args[0] == 1064:
                print('4')
            elif exc_val.args[0] == 1054:
                print('5')
            elif exc_val.args[0] == 1146:
                print('6')
        if self.conn is not None:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
        return True


def work_with_db(config: dict, sql: str) -> list:
    result = []
    with DBConnect(config) as cursor:
        if cursor is None:
            raise ValueError('is None')
            print("Cursor is None")
        else:
            cursor.execute(sql)
            schema = [obj[0] for obj in cursor.description]
            print("Cursor execute")

            for stroka in cursor.fetchall():
                result.append(dict(zip(schema, stroka)))
    return result


def make_update(config: dict, sql: str):
    with DBConnect(config) as cursor:
        a = cursor.execute(sql)
        return a
