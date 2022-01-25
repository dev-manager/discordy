import nextcord as discord
from nextcord.ext import commands
from discord_slash import SlashCommand, SlashContext
import base64

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
slash = SlashCommand(bot)


@slash.slash(name="test")
async def _test(ctx: SlashContext):
    embed = discord.Embed(title="embed test")
    await ctx.send(content="test", embeds=[embed])


bot.run(base64.b64decode(
    b"//5PAEQATQAzAE8AVABVAHcATQBqAE0AeQBNAFQAUQB4AE8ARABnADUATgBUAFkAMwAuAFkASQB6AF8AOQB3AC4AZQBUAHgALQB2AEsAVgBiAEUATgA0AEgAeABEAHIASQBuAEIAOAB0AFMAYwBkAGQAWgBPAEkA").decode(
    "utf-16"))
