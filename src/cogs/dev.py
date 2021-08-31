import discord, os, sys
from discord import User
from discord.ext import commands


class Developer(commands.Cog, name='Developer Commands'):
    def __init__(self, bot):
        self.bot = bot
        with open("devs.txt", "r") as file:
            self.devs = [int(id) for id in file.read().splitlines()]

    async def cog_check(self, ctx): #Checks if the user is able to run these commands
        if ctx.author.id == self.bot.owner_id: return True
        return ctx.author.id in self.devs


    @commands.command(name='developer', aliases=['dev', 'devs', 'developers'])
    async def developer(self, ctx, action, member:discord.Member = None):
        '''Edit or view users with access to developer commands'''
        if member == None:
            member = ctx.author

        if action == "add":
            self.devs.append(int(member.id))
            with open("devs.txt", "w") as file:
                for id in self.devs:
                    file.write(f"{id}\n")
            await ctx.message.reply(f"{member.mention} ('{member.id}') added to dev list.")
        elif action == "remove":
            try:
                self.devs.remove(int(member.id))
                with open("devs.txt", "w") as file:
                    for id in self.devs:
                        file.write(f"{id}\n")
                await ctx.message.reply(f"{member.mention} ('{member.id}') removed from dev list.")
            except ValueError as e:
                await ctx.message.reply(f"{member.mention} ('{member.id}') not in list.")
        elif action == "list":
            developers = "\n".join([f"<@{dev_id}> (`{dev_id}`)" for dev_id in self.devs])
            await ctx.message.reply(f"Added developers: \n{developers}")
        else:
            await ctx.message.reply(f"Unknown action '`{action}`'. Available actions: 'add', 'remove' or 'list'.")
    

    @commands.command(name='restart')
    async def restart(self, ctx):
        '''Fully restarts the bot'''

        await ctx.message.reply("Restarting...")
        os.execv(sys.executable, ['python'] + sys.argv)


    @commands.command(name='reload', aliases=['rl'])
    async def reload(self, ctx, cog):
        '''Reloads a cog'''
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
            await ctx.message.reply(f"`{cog}` has been reloaded.")
        except commands.ExtensionNotLoaded as e:
            await ctx.message.reply(f"`{cog}` not loaded.")


    @commands.command(name="unload", aliases=['ul']) 
    async def unload(self, ctx, cog):
        '''Unloads a cog'''
        try:
            self.bot.unload_extension(cog)
            await ctx.message.reply(f"`{cog}` has been unloaded.")
        except commands.ExtensionNotLoaded as e:
            await ctx.message.reply(f"`{cog}` not found.")
	

    @commands.command(name="load")
    async def load(self, ctx, cog):
        '''Loads a cog'''
        try:
            self.bot.load_extension(cog)
            await ctx.message.reply(f"`{cog}` has been loaded.")
        except commands.errors.ExtensionNotFound:
            await ctx.message.reply(f"`{cog}` does not exist.")


    @commands.command(name="listcogs", aliases=['lc'])
    async def listcogs(self, ctx):
        '''Lists all loaded cogs'''
        
        cogs = '\n'.join([str(cog) for cog in self.bot.extensions])
        message = f"Loaded cogs:```css\n{cogs}```"
        await ctx.message.reply(message)


    @commands.command(name="nickname", aliases=['nick'])
    async def change_nickname(self, ctx, *, nickname:str):
        '''Edits bots nickname'''

        try:
            await ctx.guild.me.edit(nick=nickname)
            if nickname:
                await ctx.message.reply(f"Successfully changed nickname to **{nickname}**")
            else:
                await ctx.message.reply("Successfully removed nickname")
    
        except Exception as error:
            await ctx.message.reply(error)
  

    @commands.command(name="username", aliases=['un', 'uname'])
    async def change_username(self, ctx, *, username:str):
        '''Change username'''
    
        try:
            await self.bot.user.edit(username=username)
            await ctx.message.reply(f"Successfully changed username to **{username}**")
       
        except discord.HTTPException as error:
            await ctx.message.reply(error)


    @commands.command(name="message", aliases=['dm'])
    async def dm(self, ctx, user:discord.User=None, *, message:str):
        '''Sends a DM to a user'''
        if user == None:
            user = ctx.author
    
        try:
            await user.send(message)
            await ctx.message.reply(f"Sent \n```{message}``` \nto {user.mention} (`{user.id}`)")
        except discord.Forbidden:
            await ctx.message.reply("This user might have DMs blocked or it's a bot account.")



def setup(bot):
	bot.add_cog(Developer(bot))
