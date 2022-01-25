import asyncio
import random


async def hol_jjak(ctx, emojis, wallet, bot):
    def check(reaction, user):
        return user == ctx.author and str(reaction) in ['<:all_in:843788488385232897>',
                                                        '<:100:843788365860962324>',
                                                        '<:1000:843788366662860810>',
                                                        '<:10000:843787291675328533>']

    def check2(reaction, user):
        return user == ctx.author and str(reaction) in ['<:hol:843804087912890409>',
                                                        '<:jjak:843804087938187294>']

    def check3(reaction, user):
        return user == ctx.author and str(reaction) in ['<:one_more:843814702056210452>',
                                                        '<:nono:843814701958823937>']

    msg = await ctx.channel.send(ctx.author.mention + ' 베팅 금액을 선택해 주세요')
    await msg.add_reaction(emojis[0])
    await msg.add_reaction(emojis[1])
    await msg.add_reaction(emojis[2])
    await msg.add_reaction(emojis[3])
    author_money = wallet.get_money(ctx)
    is_hol = False
    is_jjak = False

    betting_money = 0
    try:
        msg = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.message.delete()
    else:
        bettings = msg[0].emoji.id
        if bettings == emojis[0].id:
            betting_money = 100
        elif bettings == emojis[1].id:
            betting_money = 1000
        elif bettings == emojis[2].id:
            betting_money = 10000
        elif bettings == emojis[3].id:
            betting_money = wallet.get_money(ctx)

        if betting_money - 1 >= wallet.get_money(ctx) or betting_money - 1 <= 0:
            await ctx.channel.send(ctx.author.mention + "님 베팅 금액이 자본금보다 부족합니다.")
        else:
            try:
                msg = await ctx.channel.send(ctx.author.mention + ' 홀, 짝을 선택해 주세요')
                await msg.add_reaction(emojis[4])
                await msg.add_reaction(emojis[5])
                msg = await bot.wait_for('reaction_add', timeout=60.0, check=check2)
            except asyncio.TimeoutError:
                await ctx.message.delete()
            else:
                bettings = msg[0].emoji.id
                if bettings == emojis[4].id:
                    is_hol = True
                elif bettings == emojis[5].id:
                    is_jjak = True
                bool_ = random.choice([True, False])
                if bool_ and is_hol:
                    msg = await ctx.channel.send(content=ctx.author.mention + f' {betting_money}원을 얻으셨습니다')
                    wallet.money_update(ctx, betting_money + author_money)
                    await msg.add_reaction(emojis[6])
                    await msg.add_reaction(emojis[7])
                    try:
                        msg = await bot.wait_for('reaction_add', timeout=60.0, check=check3)
                    except asyncio.TimeoutError:
                        await ctx.message.delete()
                    else:
                        if msg[0].emoji.id == 843814701958823937:
                            pass
                        elif msg[0].emoji.id == 843814702056210452:
                            await hol_jjak(ctx, emojis, wallet, bot)
                elif not bool_ and is_jjak:
                    msg = await ctx.channel.send(content=ctx.author.mention + f' {betting_money}원을 얻으셨습니다')
                    wallet.money_update(ctx, betting_money)
                    await msg.add_reaction(emojis[6])
                    await msg.add_reaction(emojis[7])
                    try:
                        msg = await bot.wait_for('reaction_add', timeout=60.0, check=check3)
                    except asyncio.TimeoutError:
                        await ctx.message.delete()
                    else:
                        if msg[0].emoji.id == 843814701958823937:
                            pass
                        elif msg[0].emoji.id == 843814702056210452:
                            await hol_jjak(ctx, emojis, wallet, bot)
                else:
                    msg = await ctx.channel.send(content=ctx.author.mention + f' {betting_money}원을 잃으셨습니다')
                    wallet.money_update(ctx, betting_money * -1)
                    await msg.add_reaction(emojis[6])
                    await msg.add_reaction(emojis[7])
                    try:
                        msg = await bot.wait_for('reaction_add', timeout=60.0, check=check3)
                    except asyncio.TimeoutError:
                        await ctx.message.delete()
                    else:
                        if msg[0].emoji.id == 843814701958823937:
                            pass
                        elif msg[0].emoji.id == 843814702056210452:
                            await hol_jjak(ctx, emojis, wallet, bot)
