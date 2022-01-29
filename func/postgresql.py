import psycopg2 as ps
from hashlib import sha512
from time import time
import pickle
import dotenv
import os
import dhooks


class UserWallet:

    def __init__(self):
        self.ins_user_sql = 'insert into main.users values({}, {}, {}, {})'
        self.select_user_sql = 'select * from main.users'
        self.update_user_sql = "update main.users set {} = {} where user_id='{}'"
        self.ins_stock_sql = 'insert into main.stock values({}, {}, {}, {}, {}, {}, {}, {}, {}, {})'
        self.select_stock_sql = 'select * from main.stock'
        self.update_stock_sql = "update main.stock set {}={} where user_id='{}'"
        self.dict = {"google": 0, "tesla": 1, "microsoft": 2, "apple": 3,
                     "amazon": 4, "netflix": 5, "disney": 6, "amd": 7, "intel": 8}
        self.dict2 = {"google": 3, "tesla": 1, "microsoft": 0, "apple": 5,
                      "amazon": 7, "netflix": 9, "disney": 8, "amd": 6, "intel": 4}
        self.hash = ''
        AUTH = dotenv.dotenv_values(dotenv_path=r'C:\discordy\auth.env', verbose=True)
        try:
            db_name = str(AUTH["db_name"])
            db_username = str(AUTH["db_user"])
            db_pwd = str(AUTH["db_pwd"])
            db_host = str(AUTH["db_host"])
            self.conn = ps.connect(dbname=db_name, user=db_username,
                                   password=db_pwd, host=db_host)
            self.cursor = self.conn.cursor()
        except psycopg2.OperationalError as e:
            dhooks.Webhook(f"{AUTH.get('webhook_url')}").send(f"{e}\nDB 접속 오류")
            print(f'데이터베이스에 연결할수 없습니다\n{e}')

    async def make_wallet(self, ctx):
        if self.get_one(ctx) is None:
            self.cursor.execute(self.ins_user_sql.format(str(ctx.author.id), 50000, 0, 0, 0))
            self.cursor.execute(self.ins_stock_sql.format(str(ctx.author.id), 0, 0, 0, 0, 0, 0, 0, 0, 0))
            self.conn.commit()
            await ctx.channel.send(ctx.author.mention + "님의 지갑이 생성되었습니다.\n현재 잔액은 50,000$입니다.")
        else:
            await ctx.channel.send(ctx.author.mention + "님의 지갑이 생성되어있습니다.")

    def money_update(self, ctx, money):
        query_data = self.get_one(ctx)[1]
        author_money = query_data
        money += author_money
        self.cursor.execute(self.update_user_sql.format('money', money, str(ctx.author.id)))
        self.conn.commit()

    def make_loan(self, ctx):
        iden = ctx.author.id
        query_data = self.get_one(ctx)
        loan = query_data[2]
        loan_count = query_data[3]
        money = query_data[1]
        money += 10000
        loan += 12000
        loan_count += 1
        self.cursor.execute(self.update_user_sql.format('money', money, iden))
        self.cursor.execute(self.update_user_sql.format('loan', loan, iden))
        self.cursor.execute(self.update_user_sql.format('loan_count', loan_count, iden))
        self.conn.commit()
    
    def delete_loan(self, ctx):
        iden = ctx.author.id
        query_data = self.get_one(ctx)
        loan = query_data[2]
        money = query_data[1]
        money -= 10000
        loan -= 12000
        self.cursor.execute(self.update_user_sql.format('money', money, iden))
        self.cursor.execute(self.update_user_sql.format('loan', loan, iden))
        self.conn.commit()

    def get_all(self):
        self.cursor.execute(self.select_user_sql)
        return self.cursor.fetchall()

    def get_one(self, ctx):
        query_data = self.get_all()
        for i in query_data:
            if i[0] == str(ctx.author.id):
                return i
            else:
                pass
        return None

    def get_money(self, ctx):
        sql = f"select * from main.users where user_id='{ctx.author.id}'"
        self.cursor.execute(sql)
        money = list(self.cursor.fetchall())
        if len(money) == 1:
            return money[0][1]
        else:
            return None

    def get_stock(self, ctx):
        sql = f'select * from main.stock'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        for i in data:
            if i[0] == str(ctx.author.id):
                return i

    async def buy_stock(self, ctx, stocks, num, price):
        print(self.dict2[stocks], self.dict2, stocks)
        print(self.get_money(ctx), float(num) * price)
        stock = self.get_stock(ctx)[self.dict2[stocks]]
        if self.get_money(ctx) < float(num) * price:
            await ctx.channel.send("자금이 부족합니다.")
        else:
            self.cursor.execute(f"update main.stock set {stocks}={stock + float(num)} where user_id='{ctx.author.id}'")
            self.conn.commit()
            self.money_update(ctx, -1 * float(num) * price)
            await ctx.channel.send("매수 주문 완료.")

    async def sell_stock(self, ctx, stocks, num, price):
        print(self.get_money(ctx), float(num) * price)
        stock = self.get_stock(ctx)[self.dict2[stocks]]
        if stock > float(num):
            await ctx.channel.send("주식이 부족합니다.")
        else:
            self.cursor.execute(f"update main.stock set {stocks}={stock - float(num)} where user_id='{ctx.author.id}'")
            self.conn.commit()
            self.money_update(ctx, (float(num) * price))
            await ctx.channel.send("매도 주문 완료.")
