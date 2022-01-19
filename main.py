import base64
import datetime

from discord.ext import commands
import discord

from functions.choshung import chosung
from functions.emoji import *
from functions.main import hol_jjak
from functions.sqlite import UserWallet

bot = commands.Bot(command_prefix='!')
TOKEN = base64.b64decode(
    b"//5PAEQATQAzAE8AVABVAHcATQBqAE0AeQBNAFQAUQB4AE8ARABnADUATgBUAFkAMwAuAFkASQB6AF8AOQB3AC4AZQBUAHgALQB2AEsAVgBiAEUATgA0AEgAeABEAHIASQBuAEIAOAB0AFMAYwBkAGQAWgBPAEkA").decode(
    "utf-16")


