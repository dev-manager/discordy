import sqlite3
import jamotools
import requests
from bs4 import BeautifulSoup


def verification_word(word):
    res = requests.get(f'https://stdict.korean.go.kr/api/search.do?key=C24208995C351C45078480BC11D658B7&q={word}')
    soup = BeautifulSoup(res.text, features='xml')
    total = int(str(soup.find('total')).replace('<total>', '').replace('</total>', ''))
    if total == 0:
        return False
    elif total != 0:
        return True


def get_chosung(word: str, channel_name: str):
    char = []
    chosungs = ''
    for i in word:
        char.append(i)
    for i in char:
        chosungs += jamotools.split_syllables(i)[0:1]
    if channel_name.split('-')[1] == chosungs:
        return True
    else:
        return False


async def chosung(ctx, wallet):
    if '초성게임o' in ctx.channel.name:
        if verification_word(ctx.message.content.split(' ')[1]):
            split = ctx.message.content.split(' ')
            if get_chosung(split[1], ctx.channel.name):
                try:
                    sql = "select * from chosung where word='{}'".format(split[1])
                    query = list(wallet.cursor.execute(sql))
                except sqlite3.OperationalError:
                    query = []
                else:
                    pass
                if len(query) == 0:
                    try:
                        wallet.cursor.execute("insert into chosung values('{}')".format(split[1]))
                        wallet.conn.commit()
                    except sqlite3.OperationalError:
                        await ctx.channel.send("데이터 베이스에 연결할수 없습니다")
                    else:
                        all_data = list(wallet.cursor.execute('select * from chosung'))
                        wallet.cursor.fetchall()
                        wallet.money_update(ctx, 500)
                        await ctx.channel.send(f"{len(all_data)}번째 단어로" + ctx.author.mention + f"님의 {split[1]} 등록됨 100원 적립")
                elif len(query) >= 1:
                    await ctx.channel.send(f"{split[1]}은 이미 등록된 단어입니다")
            else:
                await ctx.channel.send('초성이 다릅니다')
        else:
            await ctx.channel.send("사전에 등재되지 않은 단어입니다")
    elif '초성게임x' in ctx.channel.name:
        split = ctx.message.content.split(' ')
        if get_chosung(split[1], ctx.channel.name):
            try:
                sql = "select * from chosung where word='{}'".format(split[1])
                query = list(wallet.cursor.execute(sql))
            except sqlite3.OperationalError:
                query = []
            else:
                pass
            if len(query) == 0:
                try:
                    wallet.cursor.execute("insert into chosung values('{}')".format(split[1]))
                    wallet.conn.commit()
                except sqlite3.OperationalError:
                    await ctx.channel.send("데이터 베이스에 연결할수 없습니다")
                else:
                    all_data = list(wallet.cursor.execute('select * from chosung'))
                    wallet.cursor.fetchall()
                    wallet.money_update(ctx, 1000)
                    await ctx.channel.send(f"{len(all_data)}번째 단어로" + ctx.author.mention + f"님의 {split[1]} 등록됨 100원 적립")
            elif len(query) >= 1:
                await ctx.channel.send(f"{split[1]}은 이미 등록된 단어입니다")
        else:
            await ctx.channel.send("초성이 다릅니다")
    else:
        await ctx.channel.send("초성게임 채널이 아닙니다")
