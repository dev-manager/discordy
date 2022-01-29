import base64
import datetime
import time

from nextcord.ext import commands
import nextcord as discord

from func.emoji import *
from func.main import hol_jjak
from func.postgresql import UserWallet
from func.stock import Stock

bot = commands.Bot(command_prefix='~')
TOKEN = base64.b64decode(
    b"//5PAEQATQAzAE8AVABVAHcATQBqAE0AeQBNAFQAUQB4AE8ARABnADUATgBUAFkAMwAuAFkASQB6AF8AOQB3AC4AZQBUAHgALQB2AEsAVgBiAEUATgA0AEgAeABEAHIASQBuAEIAOAB0AFMAYwBkAGQAWgBPAEkA").decode(
    "utf-16")
wallet = UserWallet()
emojis = None
stock = None


@bot.event
async def on_ready():
    global emojis, stock
    emojis = get_emojis(bot)
    stock = Stock(wallet, bot, emojis)
    stock.thread.start()
    print('시작 했음')


@bot.command()
async def 홀짝(ctx):
    await hol_jjak(ctx, emojis, wallet, bot)


@bot.command()
async def 지갑생성(ctx):
    await wallet.make_wallet(ctx)


@bot.command()
async def 돈(ctx):
    money = wallet.get_money(ctx)
    if money is None:
        await ctx.channel.send(ctx.author.mention + f'님의 지갑이 발견되지 않았습니다\n!지갑생성을 이용해주세요.')
    elif money is not None:
        await ctx.channel.send(ctx.author.mention + f'님의 잔고는 {money}$입니다')


@bot.command()
async def 대출(ctx):
    wallet.make_loan(ctx)
    await ctx.channel.send('대출이 완료되었습니다')


@bot.command()
async def 상환(ctx):
    wallet.delete_loan(ctx)
    await ctx.channel.send('상환이 완료되었습니다')


@bot.command()
async def 주식(ctx):
    await stock.get_stocks(ctx)


@bot.command()
async def 주가(ctx):
    await stock.get_price(ctx)


@bot.command()
async def 매수(ctx):
    await stock.buy_stock(ctx)


@bot.command()
async def 매도(ctx):
    await stock.sell_stock(ctx)


@bot.command()
async def prefix(ctx):
    old_prefix = bot.command_prefix
    new_prefix = ctx.message.content.split(' ')[1]
    if new_prefix not in ['?', '~', '#', '!', '@', '$', '=', '갓친슈갓']:
        await ctx.channel.send('? ~ # ! @ $ = 중에서 선택해주세요.')
    else:
        bot.command_prefix = new_prefix
        await ctx.channel.send(f'접두사가 {old_prefix}에서 {new_prefix}로 변경됨.')


bot.run(TOKEN)
