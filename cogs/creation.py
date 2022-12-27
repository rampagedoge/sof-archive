import discord
from discord.ext import commands
from modules import idVerify, user_input
#from main import user_input, channel_input
import modules
import asyncio

codec = {
    '🇺🇸': "North America",
    '🇧🇷': "South America",
    '🇪🇺': "Europe",
    '🇨🇳': "Asia",
    '🇦🇺': "Oceania",
    '🇿🇦': "Africa"
}

async def channel_input(bot,user, channel, lower=True, strip=True):
    answer = await bot.wait_for("message", check=lambda response: response.author == user and response.channel == channel)
    answer = answer.content
    if lower == True:
        answer = answer.lower()
    if strip == True:
        answer = answer.strip()
    return answer

class SetupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = bot.data
        self.game = bot.game

    @commands.command()
    async def test(self, ctx):
        await ctx.send("functioning! perfect!")

    @commands.command()
    async def read_data(self, ctx,id=None):
        if not idVerify(ctx.author.id): return
        if id == None:
            id = ctx.author.id
        data = await self.data.find(int(id))
        await ctx.send("Dumping data")
        if data == None:
            await ctx.send("No data to dump.")
            return
        for i,v in enumerate(data):
            await ctx.send(f"index: {i} | key: {v} | val: {data.get(v)}")
        await ctx.send("Dumped.")

    @commands.command()
    async def wipe_data(self, ctx, id=None):
        if not idVerify(ctx.author.id): return
        if id == None:
            id = ctx.author.id
        await self.data.delete(id)
        await ctx.send(f"Cleared {str(id)}.")

    
    @commands.command()
    async def claim(self, ctx):
        if await self.data.find(ctx.author.id) != None:
            return
        #if not idVerify(ctx.author.id): return
        ins = ""
        if ctx.channel.id == 1010642243260006410:
        #if ctx.channel.id == 1014748708954443918:
            ins = "nation"
        elif ctx.channel.id == 1010642268652314664:
        #elif ctx.channel.id == 1014748724691472404:
            ins = "organization"
        else:
            return
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        channel = await ctx.guild.create_text_channel(ctx.author.name + "-" + ctx.author.discriminator, category= await ctx.guild.fetch_channel(1010642015945490544), overwrites=overwrites)
        #data = modules[f"{ins}Data"]
        if ins == "nation":
            data = modules.nationData
        else:
            pass
            #data = modules.orgData
        #channel = await ctx.guild.create_text_channel(ctx.author.name + "-" + ctx.author.discriminator, category= await ctx.guild.fetch_channel(1014748500237496380), overwrites=overwrites)
        await ctx.send(embed=modules.cembed(ctx,title=f"Created your {ins}!",description=f"Complete process in {channel.mention}",color=discord.Color.green()))
        await ctx.message.add_reaction("✅")
        msg = await channel.send(f"{ctx.author.mention}, what is your {ins}'s name?")
        name = await channel_input(self.bot,ctx.author, channel, False)
        #await msg.delete()
        msg = await channel.send(f"Is '{name}' correct?")
        correct = await channel_input(self.bot,ctx.author,channel)
        if correct != "yes":
            #await msg.delete()
            await channel.send("Cancelling...")
            await asyncio.sleep(1)
            await channel.delete()
            return
        if ins == "nation":
            msg = await channel.send(f"What is the capital of {name}?")
            capitalName = await channel_input(self.bot,ctx.author,channel,False)
            msg = await channel.send(f"Is '{capitalName}' correct?")
            correct = await channel_input(self.bot,ctx.author,channel)
            if correct != "yes":
                await channel.send("Cancelling...")
                await asyncio.sleep(1)
                await channel.delete()
                return
            dist = modules.districtTemplate
            dist["name"] = capitalName
            dist["owner"] = name
            dist["buildings"].extend([modules.buildings.get("small iron quarry"),modules.buildings.get("small solar grid")])
            data['districts'].append(dist)
        embed = discord.Embed(
            title=f"Select a continent for your {ins}.",
            description=f"**Available continents**:\n:flag_us: North America\n:flag_br: South America\n:flag_eu: Europe\n:flag_cn: Asia\n:flag_za: Africa\n:flag_au: Oceania",
            color=discord.Color.blurple()
        )
        msg = await channel.send(embed=embed)
        flags = ['🇺🇸','🇧🇷','🇪🇺','🇨🇳','🇦🇺','🇿🇦']
        for flag in flags:
            await msg.add_reaction(flag)
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in flags
        reaction,user = await self.bot.wait_for('reaction_add',timeout=60.0,check=check)
        await msg.delete()
        await channel.send(":white_check_mark: Creating database entry, please be patient!")
        location = codec[str(reaction.emoji)]
        role = discord.utils.get(ctx.guild.roles,name=location)
        await ctx.author.add_roles(role)
        data['name'] = name
        data['location'] = location
        data['_id'] = ctx.author.id
        await self.data.insert(data)
        try:
            await ctx.author.edit(nick=name)
        except:
            await channel.send("Failed to set nickname, ignoring exception.")
        gameChannel = await ctx.guild.create_text_channel(name.lower().replace(" ","-"), category= await ctx.guild.fetch_channel(1010974589083459585), overwrites=overwrites)
        #gameChannel = await ctx.guild.create_text_channel(name.lower().replace(" ","-"), category= await ctx.guild.fetch_channel(1014748500237496380), overwrites=overwrites)
        
        await channel.send("Complete! Cleaning up..")
        await asyncio.sleep(1)
        await channel.delete()
        channel = self.bot.get_channel(1010642289753870436)

    @commands.command()
    async def create(self, ctx):
        await self.claim(ctx)

async def setup(bot):
    await bot.add_cog(SetupCog(bot))