from discord.ext import commands
import discord

bot_token = ""  # Enter your token here
prefix = "!"  # Here you can set prefix for the bot

client = commands.Bot(command_prefix=prefix)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    game = discord.Game(name="!suggest")
    await client.change_presence(activity=game)


@client.event
async def on_reaction_add(reaction, user):
    suggestion_author_id = int(reaction.message.embeds[0].footer.text)
    if reaction.message.author.id == client.user.id and user.id == suggestion_author_id:
        try:
            await user.dm_channel.send("You can't react to your own suggestions!")
        except:
            await user.create_dm()
            await user.dm_channel.send("You can't react to your own suggestions!")
        await reaction.message.remove_reaction(reaction.emoji, user)


@client.command()
async def suggest(ctx, *args):
    if ctx.author == client.user:
        return
    suggestion = ""
    for arg in args:
        suggestion += arg + " "

    embed = discord.Embed(description=suggestion)
    embed.set_author(name=ctx.author.name + " suggested:", icon_url=ctx.author.avatar_url)
    embed.set_footer(text=ctx.author.id)

    await ctx.message.delete()
    sent_message = await ctx.send(embed=embed)
    await sent_message.add_reaction("✅")
    await sent_message.add_reaction("❌")


client.run(bot_token)
