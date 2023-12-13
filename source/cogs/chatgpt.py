import discord
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))
from dotenv import load_dotenv
from discord.ext import commands

class ChatGPT(commands.Cog): # create a class for our cog that inherits from commands.Cog

    def __init__(self, bot):
        self.bot = bot
        self.gpt_conversations = {}

    @discord.slash_command()
    async def chat(self, ctx, *, msg):

        # Display the user embed
        embed = discord.Embed(title=msg, color=0x3498db)  # You can change the color
        # embed.add_field(name="", value=msg, inline=False)
        embed.set_footer(text=f"Message by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

        # Check if the channel has an existing GPT conversation history
        if ctx.channel.id in self.gpt_conversations:
            messages = self.gpt_conversations[ctx.channel.id]
        else:
            # If not, create a new conversation with a system message
            messages = [{"role": "system", "content":
                "You are an intelligent assistant in a Discord environment."}]

        # Add the user's message to the conversation
        messages.append({"role": "user", "content": msg})
        async with ctx.typing():
            # Generate a reply from GPT-3.5 Turbo
            chat = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
            reply = chat.choices[0].message.content

        # Add the assistant's reply to the conversation
        messages.append({"role": "assistant", "content": reply})

        # Save the updated conversation history for this channel
        self.gpt_conversations[ctx.channel.id] = messages

        # Send the reply to the Discord channel
        while len(reply) > 0:
            if len(reply) > 2000:
                await ctx.send(reply[0:2000])
                reply = reply[2000:len(reply)]
            else:
                await ctx.send(reply)
                break

    @discord.user_command()
    async def greet(self, ctx, member: discord.Member):
        await ctx.respond(f'{ctx.author.mention} says hello to {member.mention}!')

    @commands.Cog.listener() # we can add event listeners to our cog
    async def on_member_join(self, member): # this is called when a member joins the server
    # you must enable the proper intents
    # to access this event.
    # See the Popular-Topics/Intents page for more info
        await member.send('Welcome to the server!')

def setup(bot): 
    bot.add_cog(ChatGPT(bot))