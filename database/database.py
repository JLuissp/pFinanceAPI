import sqlite3 as sql
import random
from datetime import datetime, date

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
    random_transactions = [random.randrange(-5495, 5495) for i in range(10)]


    random_data = [(datetime(random.randint(2010,2022), random.randint(1,12), random.randint(1,28)),f'cocepto {i+1}', 0 if random.uniform(0,1) > 0.50 else 1,0 if i<=0 else 1, i) for i in random_transactions]
    db = dataBase(PATH)
    db.create_db()
    db.add_transactions(data=random_data)
    print('done')