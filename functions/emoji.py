async def get_emojis(bot):
    hundred, thousand, ten_thousand, all_in, hol, jjak, one_more, nono, yes, no = ['', '', '', '', '', '', '', '', '', '']
    for i in bot.emojis:
        if i.name == '100':
            hundred = i
        elif i.id == 843788366662860810:
            thousand = i
        elif i.id == 843787291675328533:
            ten_thousand = i
        elif i.id == 843788488385232897:
            all_in = i
        elif i.id == 843804087938187294:
            jjak = i
        elif i.id == 843804087912890409:
            hol = i
        elif i.id == 843814701958823937:
            nono = i
        elif i.id == 843814702056210452:
            one_more = i
        elif i.name == "o_k":
            yes = i
        elif i.name == "cancel":
            no = i
        else:
            pass
    
    emojis = [hundred, thousand, ten_thousand, all_in, hol, jjak, one_more, nono, yes, no]
    return emojis
