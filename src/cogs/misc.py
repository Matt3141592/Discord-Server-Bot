import discord, asyncio
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType

modmail_guild_id = [829495730464882738]


class Misc(commands.Cog, name="Miscellaneous commands"):
  
    def __init__(self, bot):
        self.bot = bot
  

    @commands.command(name="ban")
    @commands.has_role(829495730464882741) #Staff on modmail server
    async def ban(self, ctx):
        messages = []
        for i in range(4):
            message = await ctx.send("ban")
            messages.append(message)
        
        await asyncio.sleep(1)
        
        for message in messages:
            await message.delete()


    @cog_ext.cog_slash(name="ping", description="Gets the bots ping", guild_ids=modmail_guild_id)
    async def ping(self, ctx:SlashContext):
        await ctx.reply(f'Pong! In {round(self.bot.latency * 1000)}ms')
	
    @cog_ext.cog_slash(name="ping", description="Gets the bots ping", guild_ids=modmail_guild_id)
    async def ping(self, ctx:SlashContext):
        await ctx.reply(f'Pong! In {round(self.bot.latency * 1000)}ms')

        
def setup(bot):
	bot.add_cog(Misc(bot))
  
