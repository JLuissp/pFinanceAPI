import sqlite3 as sql

class dataBase():
    def __init__(self, PATH):
        self.PATH = PATH

    def create_db(self):

        _connect = sql.connect(self.PATH)

        _cursor = _connect.cursor()

        _cursor.executescript('''

            DROP TABLE IF EXISTS Transactions;
            
            CREATE TABLE Transactions(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                date TEXT,
                concept TEXT,
                pay_method INTEGER,
                transaction_type INTEGER,
                amount REAL
            );
        '''
        )
        _connect.commit()
        _cursor.close()

    def add_transactions(self, data):

        _connect = sql.connect(self.PATH)
        _cursor = _connect.cursor()

        _connect.executemany("""INSERT INTO Transactions(date, concept, pay_method, transaction_type, amount) VALUES (?, ?, ?, ?, ?)""", data)
        _connect.commit()
        _cursor.close()

    def delete_transactions(self, data):
        _connect = sql.connect(self.PATH)
        _cursor = _connect.cursor()
        #for id_ in data:
        #_connect.executemany("DELETE FROM transactions WHERE id = ?", data)
        _connect.commit()
        _cursor.close()





if __name__ == '__main__':
    PATH = 'database/Transactions.sqlite3'

    #datetime.now(tz=timezone(-timedelta(hours=5))).strftime("%Y-%m-%d %H:%M:%S")
    dataBase(PATH).create_db()
    print('done')