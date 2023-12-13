import discord
from discord.ext import commands
from dotenv import load_dotenv
import subprocess

class CommandRunner(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @discord.slash_command() # we can also add application commands
    async def run(self, ctx, *, msg):

        load_dotenv("../credentials/credentials.env")
        discord_key = int(os.getenv("DISCORD_AUTHOR_ID"))
        
        if ctx.author.id == discord_key:
            # Display the user embed
            embed = discord.Embed(title=f">{msg}", color=0x41fc03)  # You can change the color
            await ctx.send(embed=embed)

            async with ctx.typing():
                result = subprocess.run(msg, capture_output=True, text=True,shell=True)

                if result.stderr != "":
                    truncated = ""
                    if len(result.stderr) > 1024:
                        truncated = "(truncated)"

                    error_embed = discord.Embed(title=f"Error: ({result.returncode}) {truncated}", color=0xFF0000)  # You can change the color
                    error_embed.add_field(name="", value=f"```{result.stderr[0:1024]}```", inline=False)
                    await ctx.send(embed=error_embed)

                if result.stdout != "":
                    truncated = ""
                    if len(result.stdout) > 1024:
                        truncated = "(truncated)"

                    output_embed = discord.Embed(title=f"Output {truncated}:", color=0x41fc03)  # You can change the color
                    output_embed.add_field(name="", value=f"```{result.stdout[0:1024]}```", inline=False)
                    await ctx.send(embed=output_embed)

                if result.stdout == "" and result.returncode:
                    output_embed = discord.Embed(title=f"Success: {result.returncode}: ", color=0x41fc03)  # You can change the color
                    


        else:
            embed = discord.Embed(title=f"You tried running: {msg}", color=0xFF0000)
            embed.set_footer(text=f"Naughty naughty {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

            await ctx.send(embed=embed)

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(CommandRunner(bot)) # add the cog to the bot