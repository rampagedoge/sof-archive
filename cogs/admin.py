import discord
from discord.ext import commands
from modules import idVerify
import modules

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = bot.data
        self.game = bot.game
    @commands.command()
    async def turn_update(self, ctx):
        if not idVerify(ctx.author.id): return
        data = await self.data.get_all()
        for player in data:
            if player['type'] == 'nation':
                for dist in player['districts']:
                    for building in dist['buildings']:
                        if building['type'] == "production":
                            for _, resource in enumerate(building['production']):
                                change = building['production'][resource]
                                await self.data.update_dict(player['_id'],'resources',resource,player['resources'][resource] + change)
                                player = await self.data.find(player['_id'])
        channel = self.bot.get_channel(1011818815388139661)
        #channel = self.bot.get_channel(1014748341453738016)
        game = await self.game.find(1)
        turn = game['turn']
        await self.game.increment(1,1,'turn')
        embed = discord.Embed(title="It is now the next turn.",description=f"Now on turn {turn+1}, and the year is... actually wait I forgot nevermind.",color=discord.Color.green())
        embed.set_footer(text="ok now go do something idk",icon_url="https://cdn.discordapp.com/avatars/1010706026112241776/1796c013a1e72e35e35dae51f3029f11.webp?size=1024")
        await channel.send(embed=embed)
async def setup(bot):
    await bot.add_cog(AdminCog(bot))