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


@client.event
async def on_ready():
    print("logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!송금'):
        text = message.content.split(' ')
        money_dict[message.author.name] = money_dict[message.author.name] - int(text[2])
        money_dict[text[1]] = money_dict[text[1]] + int(text[2])
        await message.channel.send('{}님이 {}에게 {}원을 송금하셨습니다.'.format(message.author.mention, text[1], text[2]))
    
    if message.content.startswith('!홀짝'):
        print(money_dict)
        splited = message.content.split(' ')
        bat = splited[1]
        money = splited[2]
        if bat == '홀':
            bat = 1
        elif bat == '짝':
            bat = 0
        else:
            await message.channel.send('홀, 짝을 올바르게 입력해주세요')
        result_bat = random.randint(1, 10)
        if result_bat % 2 == bat and money_dict[message.author.name] <= int(money):
            money_dict[message.author.name] = money_dict[message.author.name] + int(money)
            await message.channel.send('{}님 {}원을 얻으셨습니다'.format(message.author.mention, money))
        elif result_bat % 2 == bat and money_dict[message.author.name] <= int(money):
            money_dict[message.author.name] = money_dict[message.author.name] - int(money)
            await message.channel.send('{}님 {}원을 잃으셨습니다'.format(message.author.mention, money))
        elif money_dict[message.author.name] > int(money):
            await message.channel.send('잔고와 같거나 적은 금액을 베팅해주세요')


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
