from discord.ext import commands
import base64
from discord_slash import SlashCommand # Importing the newly installed library.
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle

buttons = [
    create_button(style=ButtonStyle.green, label="A green button"),
    create_button(style=ButtonStyle.blue, label="A blue button")
]
action_row = create_actionrow(*buttons)



TOKEN = base64.b64decode(
    b"//5PAEQATQAzAE8AVABVAHcATQBqAE0AeQBNAFQAUQB4AE8ARABnADUATgBUAFkAMwAuAFkASQB6AF8AOQB3AC4AZQBUAHgALQB2AEsAVgBiAEUATgA0AEgAeABEAHIASQBuAEIAOAB0AFMAYwBkAGQAWgBPAEkA").decode(
    "utf-16")
client = commands.Bot(command_prefix="!")
slash = SlashCommand(client, sync_commands=True) # Declares slash commands through the client.


@client.event
async def on_ready():
    client.http.send_message()
    print("Ready!")


@slash.slash(name="test")
async def _test(ctx):
    await ctx.send("test", components=[action_row])
    
client.run(TOKEN)