from django.db import connection


class ExecRawQuery:
    def __int__(self):
        pass

    @staticmethod
    def execute(query):
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = ExecRawQuery.dict_fetch_all(cursor)

    @staticmethod
    def select_raw_query(query):
        rows = dict()

        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = ExecRawQuery.dict_fetch_all(cursor)

        return rows

    @staticmethod
    def dict_fetch_all(cursor):
        desc = cursor.description

        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
