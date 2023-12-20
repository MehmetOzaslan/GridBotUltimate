from dotenv import load_dotenv
import discord
from discord.ext import commands

import os

if __name__ == '__main__':
    # Load the environment variables from the .env file
    load_dotenv("../credentials/credentials.env")

    # Read the variables
    discord_key = os.getenv("DISCORD_KEY")

    
    bot = commands.Bot()
    bot.load_extension('cogs.command_runner')
    bot.load_extension('cogs.chatgpt')
    bot.load_extension('cogs.pvc_query_wrapper')
    bot.run(discord_key)





    

