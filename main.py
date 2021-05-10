# -*- coding: utf-8 -*-
import discord
import random
import pickle
import base64

logging_file = open('message.log', 'w')
logging_file.write('logging start\n')

token = base64.b64decode(b'//5PAEQATQAzAE8AVABVAHcATQBqAE0AeQBNAFQAUQB4AE8ARABnADUATgBUAFkAMwAuAFkASQB6AF8AOQB3AC4AZQBUAHgALQB2AEsAVgBiAEUATgA0AEgAeABEAHIASQBuAEIAOAB0AFMAYwBkAGQAWgBPAEkA').decode('utf-16')
client = discord.Client()

money_file = open('money.db', 'rb')
loan_file = open('loan.db', 'rb')
loan_count_file = open('loan_count.db', 'rb')
percent_file = open('percent.db', 'rb')

money_dict = pickle.load(money_file)
loan_dict = pickle.load(loan_file)
loan_count_dict = pickle.load(loan_count_file)
percent = pickle.load(percent_file)

money_file.close()
loan_file.close()
loan_count_file.close()
percent_file.close()


@client.event
async def on_ready():
    print("logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    print(message.content, message.author)
    print(f'{message.author.name} - {message.content.encode("utf-8")}', file=logging_file, flush=True)

    if message.author == client.user:
        return

    if message.content.startswith('소라고둥님?'):
        choices = message.content.split(' ')[1:]
        if '동쿠란보를' in choices or '사쿠란보를' in choices or '동쿠란보' in choices or '사쿠란보' in choices:
            await message.channel.send('절대 안돼.')
        else:
            messages = ["언젠가는.", "가만히 있어.", "다 안돼.", "그것도 안돼.", "그럼.", "다시 한 번 물어봐.", "안돼.", "절대 안돼."]
            choice = random.sample(messages, k=1)
            await message.channel.send(choice[0])
        
    if message.content.startswith('!종료'):
        if message.author.guild_permissions.manage_guild:
            money_file = open('money.db', 'wb')
            loan_file = open('loan.db', 'wb')
            loan_count_file = open('loan_count.db', 'wb')
            percent_file = open('percent.db', 'wb')
    
            pickle.dump(money_dict, money_file)
            await message.channel.send('잔고 db 백업 완료')
            pickle.dump(loan_dict, loan_file)
            await message.channel.send('대출 db 백업 완료')
            pickle.dump(loan_count_dict, loan_count_file)
            await message.channel.send('대출 횟수 db 백업 완료')
            pickle.dump(percent, percent_file)
            await message.channel.send('퍼센트 db 백업 완료')
    
            money_file.close()
            loan_file.close()
            loan_count_file.close()
            percent_file.close()
            await message.channel.send('안녕히 계세요 여러분')
            exit(1)
        elif not message.author.guild_permissions.manage_guild:
            await message.channel.send('서버 관리자 권한이 필요합니다')
    
    if message.content.startswith('!백업'):
        if message.author.guild_permissions.manage_guild:
            money_file = open('money.db', 'wb')
            loan_file = open('loan.db', 'wb')
            loan_count_file = open('loan_count.db', 'wb')
            percent_file = open('percent.db', 'wb')
            
            pickle.dump(money_dict, money_file)
            await message.channel.send('잔고 db 백업 완료')
            pickle.dump(loan_dict, loan_file)
            await message.channel.send('대출 db 백업 완료')
            pickle.dump(loan_count_dict, loan_count_file)
            await message.channel.send('대출 횟수 db 백업 완료')
            pickle.dump(percent, percent_file)
            await message.channel.send('퍼센트 db 백업 완료')
            
            money_file.close()
            loan_file.close()
            loan_count_file.close()
            percent_file.close()
        elif not message.author.guild_permissions.manage_guild:
            await message.channel.send('서버 관리자 권한이 필요합니다')

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
        try:
            if loan_count_dict[message.author.name] >= 10:
                await message.channel.send('게임오버 되셨습니다 {}님\n모든 지갑및 정보들이 사라지며 지갑 재생성을 통해 재시작할 수 있습니다\n게임을 재시작 하려면 !지갑 생성을 입력해 주세요'.format(message.author.mention))
                del money_dict[message.author.name]
                del loan_dict[message.author.name]
                del loan_count_dict[message.author.name]
                
            else:
                amount = message.content.split(' ')
                if len(amount) == 1:
                    await message.channel.send(message.author.mention + '님 의 대출 가능 횟수는 {}번 입니다'.format(10 - loan_count_dict.get(message.author.name)))
                
                else:
                    if amount[1].startswith('-'):
                        await message.channel.send('음수는 대출 불가능합니다')
                    else:
                        if not len(amount[1]) >= 6:
                            amount = amount[1]
                            loan_dict[message.author.name] += round(round(int(amount) + (int(amount) * (0.05 * len(amount)))))
                            money_dict[message.author.name] += int(amount)
                            loan_count_dict[message.author.name] += 1
                            print(loan_dict, loan_count_dict, money_dict)
                            await message.channel.send(message.author.mention + '님 {}원 이자 {}원으로 대출 완료 되었습니다'.format(amount, round(int(amount) + (int(amount) * (0.05 * len(amount))))))
                            await message.channel.send(message.author.mention + '님 의 대출 가능 횟수는 {}번 입니다'.format(10 - loan_count_dict.get(message.author.name)))
                        else:
                            amount = amount[1]
                            loan_dict[message.author.name] += round(int(amount) + int(amount) * 0.05)
                            money_dict[message.author.name] += int(amount)
                            loan_count_dict[message.author.name] += 1
                            print(loan_dict, loan_count_dict, money_dict)
                            await message.channel.send(message.author.mention + '님 {}원 이자 {}원으로 대출 완료 되었습니다'.format(amount, round(int(amount) + int(amount) * 0.05)))
                            await message.channel.send(message.author.mention + '님 의 대출 가능 횟수는 {}번 입니다'.format(10 - loan_count_dict.get(message.author.name)))
        except KeyError:
            await message.channel.send(message.author.mention + '님의 지갑이 존재하지 않습니다')
    if message.content.startswith('!확률'):
        await message.channel.send('홀:{}, 짝:{}'.format(round(percent.count('홀') / len(percent) * 100, 3), round(percent.count('짝') / len(percent) * 100)), 3)
    
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
        
        elif splited[1] == '홀짝':
            await message.channel.send('고니: 싸늘하다. 가슴에 비수가 날아와 꽂힌다. 하지만 걱정하지 마라. 손은 눈보다 빠르니까. 아귀한테 밑에서 한 장, 정마담도 밑에서 한 장, 나 한 장. 아귀한테 다시 밑에서 한 장, 이제 정마담에게 마지막 한 장... \n아귀: 동작 그만 밑장빼기냐?\n고니: 뭐야.\n아귀: 내 패하고 정 마담 패를 밑에서 뺐지? 내가 빙다리 핫바지로 보이냐 이 새끼야.\n고니: 증거 있어?\n아귀: 증거? 증거 있지! 너는 나한테 9땡을 줬을 것이여. 그리고 정마담한테 줄려는 이거 이거, 이거 장짜리 아니여? 자, 모두들 보쇼. 정마담한테 장땡을 줘서 이 판을 끝내겠다, 이거 아녀?\n고니: 시나리오 쓰고 있네, 미친 새끼가!\n아귀: 으허허허허허허허\n호구: 예림이! 그 패 봐봐. 혹시 장이야?\n아귀: 패 건들지 마! 손모가지 날라가분께. 해머 갖고 와!\n정마담: 정말 이렇게까지 해야 해?\n고니: 잠깐. 그렇게 피를 봐야겠어?\n아귀: 구라치다 걸리면 피 보는 거 안 배웠냐?\n고니: 좋아. 이 패가 단풍이 아니라는 거에 내 돈 모두하고 내 손모가지 건다. 쫄리면 뒈지시든지.\n아귀: 이 Tlqkf놈이 어디서 약을 팔어?\n고니: Tlqkf, 천하의 아귀가 혓바닥이 왜 이렇게 길어? 후달리냐?\n아귀: 후달려? 으허허허허허. 오냐, 내 돈 모두하고 내 손모가지를 건다. 둘 다 묶어.\n아귀: 준비됐어? 까볼까? 자, 지금부터 확인 들어가겄습니다. 따라라란 따라란 따라란 딴 쿵작짜쿵작짜 따라리라라리\n선장: 사쿠라네!\n호구: 사쿠라야?\n아귀: 내가 봤어. 이 Tlqkf놈 밑장 빼는 걸 똑똑히 봤다니께?\n고니: 확실하지 않으면 승부를 걸지 마라 이런 거 안 배웠어? 뭐해, 니네 형님 손 안 찍고.\n아귀: 야, 이 Tlqkf놈 손모가지 찍어!')
        
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
            await message.channel.send(message.author.mention + ' 님의 잔고는 {}원 입니다.\n{} 님의 상환금은 {}원 입니다'.format(money_dict.get(message.author.name), message.author.mention, loan_dict.get(message.author.name)))

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
