from iexcloud.stock import Stock as iexStock
import nextcord
import json
import yfinance
import threading
import asyncio
import dotenv
import psycopg2 as ps


class Stock:
    def __init__(self, db, bot, emojis):
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
        self.thread = threading.Thread(target=self.thread_function)
        self.db = db
        self.bot = bot

        self.emojis = emojis
        self.stocks = {"google": "googl", "tesla": "tsla", "microsoft": "msft", "apple": "aapl", "amazon": "amzn",
                       "netflix": "nflx", "disney": "dis", "amd": "amd", "intel": "intc"}
        self.dict = {"google": 0, "tesla": 1, "microsoft": 2, "apple": 3,
                     "amazon": 4, "netflix": 5, "disney": 6, "amd": 7, "intel": 8}
        self.dict2 = {"3": 'google', "1": 'tesla', "0": 'microsoft', "5": 'apple',
                      "7": 'amazon', "9": 'netflix', "8": 'disney', "6": 'amd', "4": 'intel'}

    async def buy_stock(self, ctx):

        def check2(reaction, user):
            return user == ctx.author and str(reaction) in ['<:O_:936479446221877299>',
                                                            '<:_X:936479445462687834>']

        args = ctx.message.content.split(" ")
        if args[1] not in list(self.stocks.keys()):
            await ctx.channel.send("주식 이름이 데이터에 존재하지 않습니다.\n" +
                                   "Google, Tesla, Microsoft, Apple, Amazon, Netflix, Disney, Amd, Intel\n" +
                                   "중에서 오타 없이 입력해 주세요.")
        else:
            price = self.stock_price[self.dict.get(args[1])]
            msg = await ctx.channel.send(
                f"{args[1]}의 1주당 단가는 {price}$, {args[2]}주 가격 {price * float(args[2])}$입니다.\n매수를 원하신다면 O 이모지를 취소는 X 이모지를 눌러주세요.")
            await msg.add_reaction(self.emojis[10])
            await msg.add_reaction(self.emojis[11])
            try:
                msg = await self.bot.wait_for('reaction_add', timeout=60.0, check=check2)
            except asyncio.TimeoutError:
                msg.delete()
            else:
                emoji_name = msg[0].emoji.name
                if emoji_name == "O_":
                    await self.db.buy_stock(ctx, args[1], args[2], price)

    async def sell_stock(self, ctx):

        def check2(reaction, user):
            return user == ctx.author and str(reaction) in ['<:O_:936479446221877299>',
                                                            '<:_X:936479445462687834>']

        args = ctx.message.content.split(" ")
        if args[1] not in list(self.stocks.keys()):
            await ctx.channel.send("주식 이름이 데이터에 존재하지 않습니다.\n" +
                                   "Google, Tesla, Microsoft, Apple, Amazon, Netflix, Disney, Amd, Intel\n" +
                                   "중에서 오타 없이 입력해 주세요.")
        else:
            price = self.stock_price[self.dict.get(args[1])]
            msg = await ctx.channel.send(
                f"{args[1]}의 1주당 단가는 {price}$, {args[2]}주 가격 {price * float(args[2])}$입니다.\n매도를 원하신다면 O 이모지를 취소는 X 이모지를 눌러주세요.")
            await msg.add_reaction(self.emojis[10])
            await msg.add_reaction(self.emojis[11])
            try:
                msg = await self.bot.wait_for('reaction_add', timeout=60.0, check=check2)
            except asyncio.TimeoutError:
                msg.delete()
            else:
                emoji_name = msg[0].emoji.name
                if emoji_name == "O_":
                    await self.db.sell_stock(ctx, args[1], args[2], price)

    def thread_function(self):
        stock_price = []
        for i in list(self.stocks.values()):
            stock_price.append(json.loads(iexStock(i.upper(), output="json").get_price('1m'))[-1]["open"])
        self.stock_price = stock_price
        self.cursor.execute(
            f'update main.stock Set microsoft={stock_price[2]}, tesla={stock_price[1]}, google={stock_price[0]}, intel={stock_price[8]}, apple={stock_price[3]}, amd={stock_price[7]}, amazon={stock_price[4]}, disney={stock_price[6]}, netflix={stock_price[5]} where user_id=\'stock\';')
        self.conn.commit()
        threading.Timer(interval=480, function=self.thread_function)

    async def get_price(self, ctx):
        args = ctx.message.content.split(" ")
        if len(args) == 1:
            embed = nextcord.Embed(title="슬롯머신 주가 정보!", color=0x991200)
            for i in self.stock_price:
                embed.add_field(value=f"{i}$",
                                name=f"{list(self.stocks.keys())[self.stock_price.index(i)].capitalize()}", inline=True)
            await ctx.channel.send(embed=embed)
        else:
            embed = nextcord.Embed(title="슬롯머신 주가 정보!", color=0x991200)
            for i in args[1:]:
                embed.add_field(value=f"{self.stock_price[int(self.dict[i])]}$", name=f"{i.capitalize()}",
                                inline=True)
            await ctx.channel.send(embed=embed)

    async def get_stocks(self, ctx):
        stock = ['microsoft', 'tesla', 'google', 'intel', 'apple', 'amd', 'amazon', 'disney', 'netflix']
        embed = nextcord.Embed(title=ctx.author.name + "님의 주식 계좌")
        for i in zip(self.db.get_stock(ctx)[1:], stock):
            embed.add_field(name=i[1].capitalize(), value=str(i[0]) + "주", inline=True)
        await ctx.channel.send(embed=embed)
