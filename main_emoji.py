import base64
import datetime

from discord.ext import commands
import discord

from functions.choshung import chosung
from functions.emoji import *
from functions.main import hol_jjak
from functions.sqlite import UserWallet

bot = commands.Bot(command_prefix='!')
TOKEN = base64.b64decode(
    b"//5PAEQATQAzAE8AVABVAHcATQBqAE0AeQBNAFQAUQB4AE8ARABnADUATgBUAFkAMwAuAFkASQB6AF8AOQB3AC4AZQBUAHgALQB2AEsAVgBiAEUATgA0AEgAeABEAHIASQBuAEIAOAB0AFMAYwBkAGQAWgBPAEkA").decode(
    "utf-16")
wallet = UserWallet()
focus_ = {}
focus_time = {}


@bot.event
async def on_ready():
    global emojis
    emojis = await get_emojis(bot)
    print('시작 했음')
    # wallet.verification_previous_hash()
    # wallet.backup()


@bot.command()
async def 집중(ctx):
    if ctx.message.content.split(' ')[1] == '시작':
        focus_time[ctx.author.id] = datetime.datetime.now()
        focus_[ctx.author.id] = True
    elif ctx.message.content.split(' ')[1] == "끝":
        focus_[ctx.author.id] = False
        time = datetime.datetime.now() - focus_time[ctx.author.id]
        try:
            time_sec = time.seconds
        except AttributeError:
            time_sec = 0
        time_min = 0
        time_hour = 0
        if time_sec > 60:
            time_min = time_sec // 60
            time_sec = time_sec % 60
        if time_min > 60:
            time_hour = time_min // 60
            time_min = time_min % 60
        await message.channel.send(ctx.author.mention + f'님은 {time_hour}시간 {time_min}분 {time_sec}초동안 집중하셨습니다')


@bot.command()
async def 홀짝(ctx):
    global money_dict
    money_dict = hol_jjak(ctx, bot, 홀짝, emojis, wallet)


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
    await ctx.channel.send('대출이 완료되었습니다')


@bot.command()
async def 상환(ctx):
    wallet.delete_loan(ctx)
    await ctx.channel.send('상환이 완료되었습니다')

# 제거후 타 프로젝트로 이관
# @bot.command()
# async def 초성게임(ctx):
#     await chosung(ctx, wallet)


@bot.command()
async def prefix(ctx):
    old_prefix = bot.command_prefix
    new_prefix = ctx.message.content.split(' ')[1]
    if new_prefix not in ['?', '~', '#', '!', '@', '$', '=', '갓친슈갓']:
        await ctx.channel.send('아니 진짜 제발... ? ~ # ! @ $ = 안에서만....')
    else:
        bot.command_prefix = new_prefix
        await ctx.channel.send(f'My old prefix is {old_prefix}, and my new prefix is {new_prefix}')


@bot.event
async def on_message(message):
    if focus_.get(message.author.id):
        await message.channel.purge(limit=1)
        await message.channel.send(message.author.mention + ' 딴짓 멈춰!!')
    elif focus_.get(message.author.id) is None:
        focus_[message.author.id] = False
    else:
        await bot.process_commands(message)

bot.run(TOKEN)
