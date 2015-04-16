import MySQLdb


class MySQLDB:

    def __init__(self):
        self.db = MySQLdb.connect("localhost", "root", "root", "data_mining")

    def getcursor(self):
        cursor = self.db.cursor()
        return cursor

    def executequery(self, query):
        cursor = self.getcursor()
        cursor.execute(query)
        data = cursor.fetchone()
        print "%d %s" % (data[0], data[1])

    def closedb(self):
        self.db.close()
