import discord
from discord.ext import commands
import sqlite3 as sql
from dotenv import load_dotenv
import os


class PVCQueryWrapper(commands.Cog): # create a class for our cog that inherits from commands.Cog

    def __init__(self, bot):
        self.bot = bot
        self.gpt_conversations = {}

    @discord.slash_command()
    async def pvcsql(self, ctx, msg, description = "run sql selects on the player_locations table."):
        load_dotenv("../credentials/credentials.env")
        allowed = os.getenv("PVC_SQL_ALLOWED").split(',')
        pvc_db_path = os.getenv("PVC_LOG_DB_PATH")

        if str(ctx.author.id) in allowed:

            try:

                await ctx.respond(embed=discord.Embed(title="", color=0x41fc03).add_field(name="", value=f"```{msg[:1024]}```", inline=False))

                conn = sql.connect(pvc_db_path)
                result = conn.execute(msg)
                conn.commit()
                out = result.fetchall()

                # Convert the output to a string
                output_str = "\n".join(str(row) for row in out)

                if len(output_str) <= 1024:
                    # Send output in embed if it's short enough
                    embed = discord.Embed(title="SQL Query Result", description=output_str, color=discord.Color.blue())
                    await ctx.respond(embed=embed)
                else:
                    # Save to a txt file and upload if the output is too long
                    with open("output.txt", "w") as file:
                        file.write(output_str)
                    await ctx.respond(file=discord.File("output.txt"))
            
            except Exception as e:
                if len(str(e)) <= 1024:
                    # Send output in embed if it's short enough
                    embed = discord.Embed(title="ERROR", description=str(e), color=discord.Color.red())
                    await ctx.respond(embed=embed)
                else:
                    # Save to a txt file and upload if the output is too long
                    with open("output.txt", "w") as file:
                        file.write(str(e))
                    await ctx.respond(file=discord.File("output.txt"))
            


        else:
            await ctx.send("Permission Denied.")


def setup(bot): 
    bot.add_cog(PVCQueryWrapper(bot))