import discord
import dotenv
import os
import pickle
import random

dotenv.load_dotenv('.env')
token = os.environ.get('token')

client = discord.Client()
money_db = open('money.db', 'rb')
money_dict = pickle.load(money_db)
percent = []

@client.event
async def on_ready():
    print("logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!확률'):
        await message.channel.send('홀:{}, 짝:{}'.format(percent.count('홀') / len(percent) * 100, percent.count('짝') / len(percent) * 100))
    
    if message.content.startswith('!송금'):
        text = message.content.split(' ')
        if text[2].startswith('-'):
            await message.channel.send('음수는 처리 불가능 합니다.')
        elif money_dict[message.author.name] < int(text[2]):
            await message.channel.send('금액 오류')
        elif money_dict[message.author.name] > int(text[2]):
            money_dict[message.author.name] = money_dict[message.author.name] - int(text[2])
            money_dict[text[1]] = money_dict[text[1]] + int(text[2])
            await message.channel.send('{}님이 {}에게 {}원을 송금하셨습니다.'.format(message.author.mention, text[1], text[2]))
    
    if message.content.startswith('!홀짝'):
        print(money_dict)
        splited = message.content.split(' ')
        if splited[1] == '헲':
            embed = discord.Embed(title=message.author.mention + "님을 위한 헲", description="", color=0x00ff00)
            embed.add_field(name="!홀짝 <홀, 짝> <금액>", value="홀짝에 성공할경우 금액x2를 되돌려줘요", inline=True)
            embed.add_field(name="!돈", value="잔고를 확인할수 있어요", inline=True)
            embed.add_field(name="!확률", value="현재까지의 홀짝 확률을 볼수 있어요", inline=True)
            await message.channel.send(embed=embed)

        else:
            bat = splited[1]
            money = splited[2]
            if bat == '홀':
                bat = 1
            elif bat == '짝':
                bat = 0
            result_bat = random.randint(1, 10)
            if bat == 1 or bat ==0:
                if result_bat % 2 == 1:
                    percent.append('홀')
                elif result_bat % 2 == 0:
                    percent.append('짝')
                if result_bat % 2 == bat and money_dict[message.author.name] > int(money):
                    money_dict[message.author.name] = money_dict[message.author.name] + int(money)
                    await message.channel.send('{}님 {}원을 얻으셨습니다'.format(message.author.mention, money))
                elif result_bat % 2 != bat and money_dict[message.author.name] > int(money):
                    money_dict[message.author.name] = money_dict[message.author.name] - int(money)
                    await message.channel.send('{}님 {}원을 잃으셨습니다'.format(message.author.mention, money))
                elif money_dict[message.author.name] < int(money):
                    await message.channel.send('잔고와 같거나 적은 금액을 베팅해주세요')
            else:
                    await message.channel.send('홀, 짝을 올바르게 입력해주세요')


    if message.content.startswith('!돈'):
        print(money_dict)
        await message.channel.send(message.author.mention + '님의 잔고는 {}원 입니다. \n만약 잔고가 None로 표시된다면 !지갑생성을 통해 지갑을 생성해주세요'.format(money_dict.get(message.author.name)))
    
    if message.content.startswith('!지갑 생성'):
        if message.author.name in list(money_dict.keys()):
            await message.channel.send(message.author.mention + '님 지갑이 존재합니다.')
            pass
        elif message.author.name not in list(money_dict.keys()):
            money_dict[message.author.name] = 10000
            await message.channel.send(message.author.mention + '님 지갑 생성이 완료되었습니다')
        print(money_dict)

client.run(token)
