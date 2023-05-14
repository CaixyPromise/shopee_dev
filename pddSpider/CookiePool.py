import sqlite3

class CookiePool:
    def __init__(self, db_path):
        self.__conn = sqlite3.connect(db_path) 
        self.__cursor = self.__conn.cursor()
        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS Cookie_Pool 
            (
                id INTEGER not null primary key autoincrement unique,
                cookie TEXT not null unique,
                created_at TIMESTAMP default CURRENT_TIMESTAMP not null
            );''')
        self.__conn.commit()

    def add_data(self, cookie):
        try:
            self.__cursor.execute("""
                        INSERT INTO Cookie_Pool (cookie) VALUES (?)
                    """, (cookie,)
                                  )
            self.__conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def delete_data(self, _id):
        sql = 'DELETE FROM Cookie_Pool WHERE id = ?'
        self.__cursor.execute(sql, (_id,))
        self.__conn.commit()

    def update_data(self, data, _id = -1):
        sql = 'UPDATE Cookie_Pool SET cookie = ? WHERE id = ?'
        self.__cursor.execute(sql, (data, _id))
        self.__conn.commit()

    def get_all(self):
        sql = 'SELECT Cookie_Pool.id, Cookie_Pool.cookie, Cookie_Pool.created_at FROM Cookie_Pool'
        self.__cursor.execute(sql)
        rows = self.__cursor.fetchall()
        return rows

    def __add__(self, other):
        self.add_data(other)
        return 1

    def __del__(self):
        self.__cursor.close()
        self.__conn.close()
