import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
import subprocess
import tempfile
import psutil

from PIL import Image, ImageDraw, ImageFont


class CommandRunner(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot

    async def display_text_image(self, ctx, embed, msg):
        max_width = 600
        max_height = 800
        font_size = 10

        height = len(msg.split('\n')) * int(font_size*1.5)
        width = max(len(line) for line in msg.split('\n')) * int(font_size*0.75)

        img = Image.new('RGB', (width, height), color=(0, 0, 0))
        img_file = tempfile.gettempdir() + '/output.png'
        d = ImageDraw.Draw(img)

        # Use a monospace font
        font = ImageFont.truetype("DejaVuSansMono.ttf", 10)

        # Draw the text on the image
        d.multiline_text((10,10), msg, fill=(255,255,255), font=font,embedded_color=True)

        # Save the image
        img.save(img_file)        
        file = discord.File(img_file, filename="output.png")
        embed.set_image(url="attachment://output.png")

        await ctx.send(file=file, embed=embed)


    @discord.slash_command()
    async def pid(self, ctx):
        load_dotenv("../credentials/credentials.env")
        discord_key = int(os.getenv("DISCORD_AUTHOR_ID"))

        if ctx.author.id == discord_key:
            # Get current process ID and parent process ID
            pid = os.getpid()
            ppid = os.getppid()

            # Create an embed to display the information
            embed = discord.Embed(
                title="Process Information",
                color=discord.Color.blue()
            )
            embed.add_field(name="PID", value=str(pid) + " " +  psutil.Process(pid).name(), inline=False)
            embed.add_field(name="PPID", value=str(ppid) + " " + psutil.Process(ppid).name(), inline=False)

            await ctx.respond(embed=embed)
        else:
            await ctx.respond("You do not have permission to use this command.")


    @discord.slash_command() # we can also add application commands
    async def run(self, ctx, *, msg):

        load_dotenv("../credentials/credentials.env")
        discord_key = int(os.getenv("DISCORD_AUTHOR_ID"))
        
        if ctx.author.id == discord_key:

            await ctx.send(embed=discord.Embed(title="", color=0x41fc03).add_field(name="", value=f"```{msg[:1024]}```", inline=False))

            async with ctx.typing():
                process = await asyncio.create_subprocess_shell(
                    msg,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await process.communicate()

                if stderr:
                    stderr = stderr.decode()
                    if len (stderr) < 1024:
                        error_embed = discord.Embed(
                            title=f"Error: ({process.returncode})",
                            color=0xFF0000
                        )
                        error_embed.add_field(name="", value=f"```{stderr}```", inline=False)
                        await ctx.send(embed=error_embed)

                    else:
                        output_embed = discord.Embed(
                            title=f"Error: ({process.returncode}) (truncated to image)",
                            color=0xFF0000
                        )
                        await self.display_text_image(output_embed, stderr)


                if stdout:
                    stdout = stdout.decode()
                    if len(stdout) < 1024:
                        output_embed = discord.Embed(
                            title="Output:",
                            color=0x41fc03
                        )
                        output_embed.add_field(name="", value=f"```{stdout}```", inline=False)
                        await ctx.send(embed=output_embed)

                    else:
                        output_embed = discord.Embed(
                            title="Output" + (" (truncated to image):" if len(stdout) > 1024 else ":"),
                            color=0x41fc03
                        )
                        await self.display_text_image(ctx, output_embed, stdout)

                if not stdout and process.returncode == 0:
                    await ctx.send(embed=discord.Embed(title="Success", color=0x41fc03))                    


        else:
            embed = discord.Embed(title=f"You tried running: {msg}", color=0xFF0000)
            embed.set_footer(text=f"Naughty naughty {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

            await ctx.send(embed=embed)

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(CommandRunner(bot)) # add the cog to the bot