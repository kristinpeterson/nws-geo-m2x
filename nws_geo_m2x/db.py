import os
import psycopg2
import urlparse

class DB:

    def __init__(self):
        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(os.environ["DATABASE_URL"])
        self.connection = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        self.cur = self.connection.cursor()

    def execute(self, command):
        self.cur.execute(command)

    def copy_from(self, path, table, columns, sep):
        data = open(path)
        self.cur.copy_from(file=data, table=table, columns=columns, sep=sep)

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def __del__(self):
        self.cur.close()
        self.connection.close()
