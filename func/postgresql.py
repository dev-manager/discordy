import psycopg2 as ps
from hashlib import sha512
from time import time
import pickle
from dotenv import load_dotenv
from os import getenv


class UserWallet:

    def __init__(self, bot):
        self.ins_sql = 'insert into main.users values(?, ?, ?, ?)'
        self.select_sql = 'select * from main.users'
        self.update_sql = "update main.users set {} = {} where user_id='{}'"
        self.dict = ['user_id', 'money', 'loan', 'loan_count']
        self.hash = ''
        load_dotenv(".env")
        try:
            self.conn = ps.connect(dbname=f'{getenv("db_name")}', user=f'{getenv("db_user")}', password=f'{getenv("db_pwd")}', host=f'{getenv("db_host")}')
            self.cursor = self.conn.cursor()
        except Exception:
            bot.http.
            print(f'데이터베이스에 연결할수 없습니다')
    
    def make_wallet(self, ctx):
        self.cursor.execute(self.ins_sql, (str(ctx.author.id), 10000, 0, 0, 0))
        self.conn.commit()

    def money_update(self, ctx, money):
        query_data = self.get_one(ctx)[1]
        author_money = query_data
        money += author_money
        self.cursor.execute(self.update_sql.format(self.dict[1], money, str(ctx.author.id)))
        self.conn.commit()
    
    def make_loan(self, ctx):
        iden = ctx.author.id
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
        iden = ctx.author.id
        query_data = self.get_one(ctx)
        loan = query_data[self.dict.index('loan')]
        money = query_data[self.dict.index('money')]
        money -= 10000
        loan -= 12000
        self.cursor.execute(self.update_sql.format('money', money, iden))
        self.cursor.execute(self.update_sql.format('loan', loan, iden))
        self.conn.commit()

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

    def get_money(self, ctx):
        sql = f"select * from main.users where user_id='{ctx.author.id}'"
        self.cursor.execute(sql)
        money = list(self.cursor.fetchall())
        if len(money) == 1:
            return money[0][1]
        else:
            return None
