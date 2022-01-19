import asyncio
import random


async def hol_jjak(ctx, bot, hol_jjak_, emojis, wallet):
    author_money = wallet.get_money(ctx)
    is_hundred = False
    is_thousand = False
    is_ten_thousand = False
    is_all_in = False
    is_hol = False
    is_jjak = False
    
    def check(reaction, user):
        return user == ctx.message.author and str(reaction) in ['<:all_in:843788488385232897>',
                                                                '<:100:843788365860962324>',
                                                                '<:1000:843788366662860810>',
                                                                '<:10000:843787291675328533>']
    
    betting_money = 0
    msg = await ctx.channel.send(ctx.message.author.mention + ' 베팅 금액을 선택해 주세요')
    await msg.add_reaction(emojis[0])
    await msg.add_reaction(emojis[1])
    await msg.add_reaction(emojis[2])
    await msg.add_reaction(emojis[3])
    try:
        msg = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.message.delete()
    else:
        betting = msg[0].emoji.id
        if betting == emojis[0].id:
            is_hundred = True
            betting_money = 100
        elif betting == emojis[1].id:
            is_thousand = True
            betting_money = 1000
        elif betting == emojis[2].id:
            is_ten_thousand = True
            betting_money = 10000
        elif betting == emojis[3].id:
            is_all_in = True
            betting_money = wallet.get_money(ctx)
        
        def check2(reaction, user):
            global ctx
            return user == ctx.message.author and str(reaction) in ['<:hol:843804087912890409>',
                                                                    '<:jjak:843804087938187294>']
        
        def check3(reaction, user):
            global ctx
            return user == ctx.message.author and str(reaction) in ['<:one_more:843814702056210452>',
                                                                    '<:nono:843814701958823937>']
        
        try:
            msg = await ctx.channel.send(ctx.message.author.mention + ' 홀, 짝을 선택해 주세요')
            await msg.add_reaction(emojis[4])
            await msg.add_reaction(emojis[5])
            msg = await bot.wait_for('reaction_add', timeout=60.0, check=check2)
        except asyncio.TimeoutError:
            await ctx.message.delete()
        else:
            betting = msg[0].emoji.id
            if betting == emojis[4].id:
                is_hol = True
            elif betting == emojis[5].id:
                is_jjak = True
            bool_ = random.choice([True, False])
            if bool_ and is_hol:
                msg = await ctx.channel.send(content=ctx.message.author.mention + f' {betting_money}원을 얻으셨습니다')
                mongo.money_update(ctx.author.id, betting_money + author_money)
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
                        await hol_jjak_(ctx=ctx)
            elif not bool_ and is_jjak:
                msg = await ctx.channel.send(content=ctx.message.author.mention + f' {betting_money}원을 얻으셨습니다')
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
                        await hol_jjak_(ctx=ctx)
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
                        await hol_jjak_(ctx=ctx)