import discord
from discord.ext import commands
import os
from motor.motor_asyncio import AsyncIOMotorClient
from libraries.handler import Document
from modules import idVerify
import modules
from dotenv import dotenv_values

bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())
cfg = dotenv_values(".env")
@bot.event
async def on_ready():
    bot.mongo = AsyncIOMotorClient(cfg['DBKEY'])
    bot.db = bot.mongo['data']
    bot.data = Document(bot.db,'data')
    bot.game = Document(bot.db, 'gameData')
    print('Running routine game data maintenance...')
    gameData = await bot.game.find(1)
    if not gameData:
        await bot.game.insert(modules.gameTemp)
        gameData = await bot.game.find(1)
    counter = 0
    for _, key in enumerate(modules.gameTemp):
        if not key in gameData:
            val = modules.gameTemp[key]
            await bot.game.insert({'_id':1,key:val})
            counter += 1
    print(f'Resolved {counter} issues in game data!')
    print('Loading cogs...')
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded {filename}!')
    print('Successfully loaded all cogs!')
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
"""
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error,commands.CommandOnCooldown):
        embed = discord.Embed(
            title="Slow the fuck down!",
            description=f"You can use this command again in **{round(error.retry_after,2)}** seconds!",
            color=discord.Color.red()
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.set_footer(text=modules.botFooter(),icon_url="https://cdn.discordapp.com/avatars/1010706026112241776/1796c013a1e72e35e35dae51f3029f11.webp?size=1024")
        await ctx.send(embed=embed)
    elif isinstance(error,commands.CommandNotFound):
        await ctx.send("HAHA DUMBASS! THAT COMMAND DOESNT EXIST!!!")
    else:
        tb = error.__traceback__
        errLine = 0
        if tb is not None:
            errLine = tb.tb_lineno
        embed = discord.Embed(
            title=f"Caught error!",
            description=f"{error}\nLine {errLine}",
            color=discord.Color.red()
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.set_footer(text=modules.botFooter(),icon_url="https://cdn.discordapp.com/avatars/1010706026112241776/1796c013a1e72e35e35dae51f3029f11.webp?size=1024")
        await ctx.send(embed=embed)"""
@bot.command()
async def reload(ctx,cogname):
    if not idVerify(ctx.author.id): return
    if cogname == "all":
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                #await ctx.send(f"Found {filename}...")
                await bot.unload_extension(f'cogs.{filename[:-3]}')
                await bot.load_extension(f'cogs.{filename[:-3]}')
                await ctx.send(f"Reloaded {filename}!")
        return
    for filename in os.listdir('./cogs'):
        if filename == cogname + '.py':
            #await ctx.send(f"Found {cogname}.py...")
            await bot.unload_extension(f'cogs.{filename[:-3]}')
            await bot.load_extension(f'cogs.{filename[:-3]}')
            await ctx.send(f"Reloaded {cogname}.py!")

@bot.command()
async def load(ctx, cogname):
    if not idVerify(ctx.author.id): return
    for filename in os.listdir('./cogs'):
        if filename == cogname + '.py':
            #await ctx.send(f"Found {cogname}.py...")
            await bot.load_extension(f'cogs.{filename[:-3]}')
            await ctx.send(f'Loaded {cogname}.py!')

bot.run(cfg['TOKEN'])