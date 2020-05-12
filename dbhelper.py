import pymysql
import dbconfig

class DBHelper:

    def connect(self, database="crimemap"):
        return pymysql.connect(host='127.0.0.1', user=dbconfig.db_user,
                               passwd=dbconfig.db_password,
                               db=database)

    def get_all_inputs(self):
        connection = self.connect()
        try:
            SQL = "SELECT description FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(SQL)
            return cursor.fetchall()
        finally:
            connection.close()


def add_input(self, data):
    connection = self.connect()
    try:
        # The following introduces a deliberate security flaw.
        # See section on SQL injection below

        SQL = "INSERT INTO `crimes` ('description') VALUES (%s)"
        with connection.cursor() as cursor:
            cursor.execute(SQL, data)
            connection.commit()
    finally:
        connection.close()


def clear_all(self):
    connection = self.connect()
    try:
        SQL = "DELETE FROM crimes;"
        with connection.cursor() as cursor:
            cursor.execute(SQL)
            connection.commit()
    finally:
        connection.close()