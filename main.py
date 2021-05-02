import discord
import random

token = '---input token---'
client = discord.Client()
money_dict = {}
loan_dict = {}
loan_count_dict = {}
percent = []


@client.event
async def on_ready():
    print("logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!상환'):
        if loan_dict[message.author.name] == 0:
            await message.channel.send('상환할 금액이 없습니다')
        elif message.content.split(' ')[1].startswith('-'):
            await message.channel.send('음수는 상환 불가능합니다')
        else:
            amount = message.content.split(' ')
            amount = int(amount[1])
            if amount > money_dict[message.author.name]:
                await message.channel.send('잔액 이상 상환 불가능 합니다')
            else:
                loan_dict[message.author.name] -= amount
                money_dict[message.author.name] -= amount
                print(loan_dict, loan_count_dict, money_dict)
                await message.channel.send(f'{amount}원 상환 완료 원리금 합계 {loan_dict[message.author.name]}원 남았습니다')

    if message.content.startswith('!대출'):
        if loan_count_dict[message.author.name] >= 10:
            await message.channel.send('10회 이상 대출은 불가능 합니다')
        else:
            amount = message.content.split(' ')
            if len(amount) == 1:
                await message.channel.send(message.author.mention + '님 의 대출 가능 횟수는 {}번 입니다'.format(10 - loan_count_dict.get(message.author.name)))
            else:
                if amount[1].startswith('-'):
                    await message.channel.send('음수는 대출 불가능합니다')
                else:
                    amount = int(amount[1])
                    loan_dict[message.author.name] += round(int(amount) * 1.2)
                    money_dict[message.author.name] += amount
                    loan_count_dict[message.author.name] += 1
                    print(loan_dict, loan_count_dict, money_dict)
                    await message.channel.send(message.author.mention + '님 {}원 대출 완료 되었습니다'.format(amount))
                    await message.channel.send(message.author.mention + '님 의 대출 가능 횟수는 {}번 입니다'.format(10 - loan_count_dict.get(message.author.name)))

    if message.content.startswith('!확률'):
        await message.channel.send('홀:{}, 짝:{}'.format(percent.count('홀') / len(percent) * 100, percent.count('짝') / len(percent) * 100))
    
    if message.content.startswith('!송금'):
        text = message.content.split(' ')
        if text[2].isdigit():
            if text[2].startswith('-'):
                await message.channel.send('음수는 처리 불가능 합니다.')
            elif money_dict[message.author.name] < int(text[2]):
                await message.channel.send('금액 오류')
            elif money_dict[message.author.name] > int(text[2]):
                money_dict[message.author.name] = money_dict[message.author.name] - int(text[2])
                money_dict[text[1]] = money_dict[text[1]] + int(text[2])
                await message.channel.send('{}님이 {}에게 {}원을 송금하셨습니다.'.format(message.author.mention, text[1], text[2]))
        else:
            await message.channel.send('숫자만 입력해 주세요')
    
    if message.content.startswith('!홀짝'):
        print(money_dict)
        splited = message.content.split(' ')
        if splited[1] == '헲':
            embed = discord.Embed(title="헲", description="", color=0x00ff00)
            embed.add_field(name="!홀짝 <홀, 짝> <금액>", value="홀짝에 성공할경우 금액x2를 되돌려줘요", inline=True)
            embed.add_field(name="!돈", value="잔고를 확인할수 있어요", inline=True)
            embed.add_field(name="!확률", value="현재까지의 홀짝 확률을 볼수 있어요", inline=True)
            embed.add_field(name="!대출 <금액>", value="대출을 받을수 있어요, 이자는 원금의 20%에요", inline=True)
            embed.add_field(name="!상환 <금액>", value="대출 상환을 할수 있어요, 나눠서 상환할수 있으니 걱정 마세요", inline=True)
            embed.add_field(name="게임 룰", value="대출 횟수가 10회를 넘어가면 게임 오버에요\n 제한된 대출 안에서 최대한 오래 살아 남길 바래요", inline=True)
            await message.channel.send(embed=embed)

        else:
            if splited[2].isdigit():
                if splited[2].startswith('-'):
                    await message.channel.send('음수는 처리 불가능 합니다.')
                else:
                    bat = splited[1]
                    money = splited[2]
                    if bat == '홀':
                        bat = 1
                    elif bat == '짝':
                        bat = 0
                    result_bat = random.randint(1, 10)
                    if bat == 1 or bat == 0:
                        if result_bat % 2 == 1:
                            percent.append('홀')
                        elif result_bat % 2 == 0:
                            percent.append('짝')
                        if result_bat % 2 == bat and money_dict[message.author.name] >= int(money):
                            money_dict[message.author.name] = money_dict[message.author.name] + int(money)
                            await message.channel.send('{}님 {}원을 얻으셨습니다'.format(message.author.mention, money))
                        elif result_bat % 2 != bat and money_dict[message.author.name] >= int(money):
                            money_dict[message.author.name] = money_dict[message.author.name] - int(money)
                            await message.channel.send('{}님 {}원을 잃으셨습니다'.format(message.author.mention, money))
                        elif money_dict[message.author.name] < int(money):
                            await message.channel.send('잔고와 같거나 적은 금액을 베팅해주세요')
                    else:
                        await message.channel.send('홀, 짝을 올바르게 입력해주세요')
            else:
                await message.channel.send('음수는 처리 불가능 합니다.')

    if message.content.startswith('!돈'):
        print(money_dict)
        if money_dict[message.author.name] is None:
            await message.channel.send('지갑이 존재하지 않습니다 지갑을 생성해 주세요.')
        else:
            await message.channel.send(message.author.mention + '님의 잔고는 {}원 입니다.'.format(money_dict.get(message.author.name)))
            await message.channel.send(message.author.mention + '님의 상환금은 {}원 입니다.'.format(loan_dict.get(message.author.name)))

    if message.content.startswith('!지갑 생성'):
        if message.author.name in list(money_dict.keys()):
            await message.channel.send(message.author.mention + '님 지갑이 존재합니다.')
            pass
        elif message.author.name not in list(money_dict.keys()):
            money_dict[message.author.name] = 10000
            loan_count_dict[message.author.name] = 0
            loan_dict[message.author.name] = 0
            await message.channel.send(message.author.mention + '님 지갑 생성이 완료되었습니다')
        print(money_dict)

client.run(token)
