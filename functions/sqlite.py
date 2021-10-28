import sqlite3
from hashlib import sha512
from sqlite3.dbapi2 import Cursor
from time import time
import pickle


class UserWallet:
    cursor: Cursor

    def __init__(self):
        path = 'E:/discordy/database/database.db'
        self.ins_sql = 'insert into users values(?, ?, ?, ?)'
        self.select_sql = 'select * from users'
        self.update_sql = "update users set {} = {} where user_id='{}'"
        self.dict = ['user_id', 'money', 'loan', 'loan_count']
        self.hash = ''
        try:
            self.conn = sqlite3.connect(path)
            self.cursor = self.conn.cursor()
        except Exception:
            print(f'데이터베이스에 연결할수 없습니다\n{path}에 데이터베이스 파일이 있는지 확인해 주세요')
    
    def make_wallet(self, ctx):
        self.cursor.execute(self.ins_sql, (str(ctx.message.author.id), 10000, 0, 0, 0))
        self.conn.commit()

    def money_update(self, ctx, money):
        query_data = self.get_one(ctx)[1]
        author_money = query_data
        money += author_money
        self.cursor.execute(self.update_sql.format(self.dict[1], money, str(ctx.message.author.id)))
        self.conn.commit()
    
    def make_loan(self, ctx):
        iden = ctx.message.author.id
        query_data = self.get_one(ctx)
        loan = query_data[self.dict.index('loan')]
        loan_count = query_data[self.dict.index('loan_count')]
        money = query_data[self.dict.index('money')]
        money += 10000
        loan += 12000
        loan_count += 1
        self.cursor.execute(self.update_sql.format('money', money, iden))
        self.cursor.execute(self.update_sql.format('loan', loan, iden))
        self.cursor.execute(self.update_sql.format('loan_count', loan_count, iden))
        self.conn.commit()
    
    def delete_loan(self, ctx):
        iden = ctx.message.author.id
        query_data = self.get_one(ctx)
        loan = query_data[self.dict.index('loan')]
        money = query_data[self.dict.index('money')]
        money -= 10000
        loan -= 12000
        self.cursor.execute(self.update_sql.format('money', money, iden))
        self.cursor.execute(self.update_sql.format('loan', loan, iden))
        self.conn.commit()

    def insert_hash(self):
        self.cursor.execute('select * from users')
        data = str(self.cursor.fetchall())
        hashed = sha512(data.encode()).hexdigest()
        self.cursor.execute('insert into hash values(?, ?)', (round(time()), hashed[0:10]))
        self.conn.commit()
    
    def get_hash(self):
        self.cursor.execute('select * from users')
        data = str(self.cursor.fetchall())
        hashed = sha512(data.encode()).hexdigest()
        self.hash = hashed
    
    def verification_previous_hash(self):
        self.cursor.execute('select * from hash')
        data = str(self.cursor.fetchall()[-1][1])
        hashed = sha512(data.encode()).hexdigest()
        if hashed == data:
            pass
        elif hashed != data:
            print('데이터베이스가 변경됐습니다\n보안을 위해 데이터를 복원합니다')
            self.restore()

    def get_all(self):
        self.cursor.execute(self.select_sql)
        return self.cursor.fetchall()

    def get_one(self, ctx):
        query_data = self.get_all()
        for i in query_data:
            if i[0] == str(ctx.author.id):
                return i
            else:
                pass

    def backup(self):
        data = self.get_all()
        f = open('backup_data.json', 'wb')
        pickle.dump(data, f)
        f.close()
    
    def restore(self):
        f = open('backup_data.json', 'rb')
        datas = pickle.load(f)
        self.cursor.execute('drop table users')
        self.cursor.execute(
            'CREATE TABLE "users" ("user_id" TEXT NOT NULL, "money"	INTEGER NOT NULL, "loan" INTEGER NOT NULL, "loan_count"	INTEGER NOT NULL);')
        self.conn.commit()
        for data in datas:
            self.cursor.execute(self.ins_sql, data)
        self.conn.commit()
    
    def update_focus(self, ctx, is_focus):

        self.cursor.execute(self.update_sql.format('is_focus', is_focus, ctx.message.author.id))
        self.conn.commit()
    
    def is_focus(self, ctx):
        data = self.cursor.execute('select * from users where "user_id"={}'.format(ctx.author.id)).fetchall()
        print(bool(data[4]))
        return bool(data[4])
    
    def get_money(self, ctx):
        sql = f"select * from users where user_id='{ctx.author.id}'"
        money = list(self.cursor.execute(sql))
        if len(money) == 1:
            return money[0][1]
        else:
            return None
