from functions.main import hol_jjak
from functions.emoji import *
from functions.sqlite import UserWallet
from functions.choshung import chosung
import base64
from discord.ext import commands
import asyncio
import sqlite3

bot = commands.Bot(command_prefix='!')
TOKEN = base64.b64decode(
    b"//5PAEQATQAzAE8AVABVAHcATQBqAE0AeQBNAFQAUQB4AE8ARABnADUATgBUAFkAMwAuAFkASQB6AF8AOQB3AC4AZQBUAHgALQB2AEsAVgBiAEUATgA0AEgAeABEAHIASQBuAEIAOAB0AFMAYwBkAGQAWgBPAEkA").decode(
    "utf-16")
wallet = UserWallet()


@bot.event
async def on_ready():
    global emojis
    emojis = await get_emojis(bot)
    print('시작 했음')
    # wallet.verification_previous_hash()
    # wallet.backup()


@bot.command()
async def 홀짝(ctx):
    global money_dict
    money_dict = await hol_jjak(ctx, bot, 홀짝, emojis, wallet)


@bot.command()
async def 지갑생성(ctx):
    wallet.make_wallet(ctx)


@bot.command()
async def 돈(ctx):
    money = wallet.get_money(ctx)
    if money is None:
        await ctx.channel.send(ctx.author.mention + '님의 지갑이 발견되지 않았습니다')
    elif money is not None:
        await ctx.channel.send(ctx.author.mention + f'님의 잔고는 {money}원입니다')


@bot.command()
async def 대출(ctx):
    wallet.make_loan(ctx)
    ctx.channel.send('대출이 완료되었습니다')


@bot.command()
async def 상환(ctx):
    wallet.delete_loan(ctx)
    ctx.channel.send('상환이 완료되었습니다')


@bot.command()
async def 초성게임(ctx):
    await chosung(ctx, wallet)


# TODO 모빌상 + 친슈상이 장난침 인풋 필터링 당장 필수
@bot.command()
async def prefix(ctx):
    old_prefix = bot.command_prefix
    new_prefix = ctx.message.content.split(' ')[1]
    if new_prefix not in ['?', '~', '#', '!', '@', '$', '=', '갓친슈갓']:
        await ctx.channel.send('아니 진짜 제발... ? ~ # ! @ $ = 안에서만....')
    else:
        bot.command_prefix = new_prefix
        await ctx.channel.send(f'My old prefix is {old_prefix}, and my new prefix is {new_prefix}')


bot.run(TOKEN)
