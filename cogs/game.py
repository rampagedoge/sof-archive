import discord
from discord.ext import commands
import modules
from modules import user_input, cembed, idVerify
import random

class GameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = bot.data
        self.game = bot.game
    #@commands.command()
    async def nationstats(self, ctx):
        if ctx.channel.category.id != 1010974589083459585 or ctx.channel.id == 1010974684914921493: return
        #if ctx.channel.category.id != 1014748500237496380: return
        data = await self.data.find(ctx.author.id)
        resources = data['resources']
        tech = data['tech_complete']
        changes = {'energy':0,'food':0,'population':0} #Hacky solution that works so I aint complaining.
        #Find our resource changes | TODO Rewrite this, it sucks dick
        ###for building in data['buildings']:
        ###    if building['type'] == 'production':
        ###        for _, resource in enumerate(building['production']):
        ###            change = building['production'].get(resource)
        ###            if not changes.get(resource): changes[resource] = 0
        ###            changes[resource] += change
        buildingCount = 0
        for district in data['districts']:
            for building in district['buildings']:
                buildingCount += 1
                for _, resource in enumerate(building['production']):
                    change = building['production'].get(resource)
                    if not changes.get(resource): changes[resource] = 0
                    changes[resource] += change
        #Iterate each resource. We have the tech unlocked? Chuck it in the list.
        val = ""
        for _, key in enumerate(resources):
            if key == "energy" or key == "food" or key == "population": continue
            value = resources.get(key)
            resourceData = modules.resources.get(key)
            if resourceData.get('required_tech') in data['tech_complete'] or resourceData.get('required_tech') == None:
                change = changes.get(key)
                if not change: change = 0
                stri = ""
                if change > 0:
                    stri = f"+{change}"
                else:
                    stri = change
                val += f"{resourceData['name']}: {str(value)} ({stri})\n"

        embed = cembed(ctx,
            title = f"{data['name']}'s stats",
            #description=f"Industrial Score: {str(data['industry_score'])}"
            description=f"A great nation with {len(data['districts'])} district{'s' if len(data['districts']) > 1 else ''} and {buildingCount} building{'s' if buildingCount > 1 else ''}."
        )
        #BEST WAY I COULD THINK OF
        energystr = ""
        if changes['energy'] > 0:
            energystr = f"+{changes['energy']}"
        else:
            energystr = changes['energy']
        foodstr = ""
        if changes['food'] > 0:
            foodstr = f"+{changes['food']}"
        else:
            foodstr = changes['food']
        popstr = ""
        if changes['population'] > 0:
            popstr = f"+{changes['population']}"
        else:
            popstr = changes['population']
        embed.add_field(name="Basics",
            value = f"Energy: {resources['energy']} ({energystr})\nFood: {resources['food']} ({foodstr})\nPopulation: {resources['population']} ({popstr})"
        )
        
        embed.add_field(name="Resources",value=val)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def view(self, ctx, cmd):
        viewList = {
            "nationstats": self.nationstats
        }
        perList = [
            "stats"
        ]
        if not cmd in viewList and not cmd in perList:
            await ctx.send(embed=cembed(ctx,title=":x: Menu not found!",description=f"Couldn't find a menu with the name {cmd.lower()}!",color=discord.Color.red()))
            return
        if cmd in perList:
            data = await self.data.find(ctx.author.id)
            cmd = data['type']+cmd
        await viewList[cmd](ctx)
    @commands.command()
    async def set(self,ctx,obj,type,*,newVal):
        if not idVerify(ctx.author.id): return
        if type == "int": newVal = int(newVal)
        try:
            data = await self.data.find(ctx.author.id)
            await self.data.upsert({"_id":ctx.author.id,obj:newVal})
            await ctx.message.add_reaction("✅")
        except:
            await ctx.message.add_reaction("❌")
    @commands.command()
    async def build(self, ctx, *, building=None):
        if ctx.channel.category.id != 1010974589083459585 or ctx.channel.id == 1010974684914921493: return
        #if ctx.channel.category.id != 1014748500237496380: return
        if building == None: return
        data = await self.data.find(ctx.author.id)
        
        resources = data['resources']
        buildData = modules.buildings.get(building.lower())
        if not buildData:
            embed = cembed(ctx,title=":x: Building not found!",description=f"The building {building.lower()} doesn't exist!",color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        for _, resource in enumerate(buildData['cost']):
            amt = buildData["cost"][resource]
            if resources[resource] < amt:
                embed = cembed(ctx,title=":x: Can't afford this building!",description=f"You need {amt - resources[resource]} more {resource}!",color=discord.Color.red())
                await ctx.send(embed=embed)
                return
        msg = await ctx.send(embed=cembed(ctx,title=f"Choose a district to build your {building.lower()} in.",description=modules.stringifyListThruKey(data['districts'],"name"),color=discord.Color.blue()))
        choice = await user_input(self.bot,ctx.author,msg)
        district = None
        for dist in data['districts']:
            if dist["name"].lower() == choice.lower():
                district = dist
                break
        if district == None:
            await ctx.send(embed=cembed(ctx,title=":x: District not found!",description=f"Couldn't find the district {choice.lower()}!",color=discord.Color.red()))
            return
        elif district['owner'] != data['name']:
            await ctx.send(embed=cembed(ctx,title=":x: District isn't owned by you!",description=f"You don't own {district['name']}! (This shouldn't appear, so you should probably report it to a developer.",color=discord.Color.red()))
            return
        elif district['capacity'] <= len(district['buildings']):
            await ctx.send(embed=cembed(ctx,title=":x: District is at maximum capacity!",description=f"Couldn't build in {district['name']} as it has reached (or exceeded) its building limit!",color=discord.Color.red()))
            return
        for _, resource in enumerate(buildData['cost']):
            amt = buildData['cost'][resource]
            await self.data.update_dict(ctx.author.id,'resources',resource,resources[resource] - amt)
        newList = data['districts']
        for dist in newList:
            if dist["name"].lower() == choice.lower():
                dist['buildings'].append(buildData)
                break
        await self.data.upsert({"_id":ctx.author.id,'districts':newList})
        embed = cembed(ctx,title=":white_check_mark: Building constructed!",description=f"Successfully constructed a {building.title()} in {district['name']}!",color=discord.Color.green())
        await ctx.send(embed=embed)
    @commands.command()
    #@commands.cooldown(1,1800, commands.BucketType.user)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def research(self, ctx, *, tech=None):
        if ctx.channel.category.id != 1010974589083459585 or ctx.channel.id == 1010974684914921493 or tech == None: ctx.command.reset_cooldown(ctx); return
        data = await self.data.find(ctx.author.id)
        tech = tech.lower()
        if tech not in modules.technologies or tech == "devmode":
            embed = cembed(ctx,title=":x: Technology not found!",description=f"The technology {tech} doesn't exist!", color = discord.Color.red())
            await ctx.send(embed=embed)
            ctx.command.reset_cooldown(ctx)
            return
        if tech in data['tech_complete']:
            embed = cembed(ctx,title=":x: Already researched!",description=f"You have already researched {tech.title()}!", color = discord.Color.green())
            await ctx.send(embed=embed)
            ctx.command.reset_cooldown(ctx)
            return
        for obj in modules.technologies[tech]['requires']:
            if obj not in data['tech_complete']:
                embed = cembed(ctx,title=":x: Missing technology requirements!",description=f"You are missing a technology required to research this technology!", color = discord.Color.red())
                await ctx.send(embed=embed)
                ctx.command.reset_cooldown(ctx)
                return
        techChange = {
            "PHYSICS": -5
        }
        for building in data['buildings']:
            if building['type'] == "tech_production":
                for _, techType in enumerate(building['sci_points']):
                    val = building['sci_points'][techType]
                    if not techChange.get(techType):
                        techChange[techType] = val
                        continue
                    techChange[techType] -= val
        for _, techType in enumerate(techChange):
            amt = techChange[techType]
            amt = -random.randint(1,abs(amt))
            techChange[techType] = amt
        if tech not in data['tech_progression']:
            await self.data.append_dict(ctx.author.id,'tech_progression',tech,modules.technologies[tech]['sci_points'])
            data = await self.data.find(ctx.author.id)
        newDict = {}
        for _, techType in enumerate(data['tech_progression'][tech]):
            if not techChange.get(techType): continue
            newDict[techType] = data['tech_progression'][tech][techType] + techChange[techType]
            if newDict[techType] <= 0:
                newDict.pop(techType)
        if len(newDict) == 0:
            await self.data.pop_dict(ctx.author.id,'tech_progression',tech)
            await self.data.append_list(ctx.author.id,'tech_complete',tech)
            embed = cembed(ctx,title=":white_check_mark: Finished researching!",description=f"Successfully researched {tech.title()}!",color=discord.Color.green())
            await ctx.send(embed=embed)
        else:
            await self.data.update_dict(ctx.author.id,'tech_progression',tech,newDict)
            desc = ""
            for _, techType in enumerate(newDict):
                change = "0"
                if techChange.get(techType):
                    change = "+" + str(abs(techChange[techType]))
                desc += f"{modules.techTypes[techType]} | {modules.technologies[tech]['sci_points'][techType]-newDict[techType]}/{modules.technologies[tech]['sci_points'][techType]} | {change}\n"
            embed = cembed(ctx,title='Worked on researching ' + tech.title() + "!",color=discord.Color.green(),description=desc)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(GameCog(bot))