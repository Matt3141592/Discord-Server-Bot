import os, discord, typing
from discord.ext import commands
from helpers.embed import full_embed
from helpers.misc import time_ago_readable, get_id_from_thread

class ModmailCommands(commands.Cog, name='Modmail Commands'):
    """Commands to make modmail easier"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.guild = self.bot.get_guild(781979349855371314)
        self.mail_log = self.bot.get_channel(829495730644713486)
        self.year8 = discord.utils.get(self.guild.roles, name = "Year 8")
        self.year9 = discord.utils.get(self.guild.roles, name = "Year 9")
        self.year10 = discord.utils.get(self.guild.roles, name = "Year 10")
        self.year11 = discord.utils.get(self.guild.roles, name = "Year 11")
        self.year12 = discord.utils.get(self.guild.roles, name = "Year 12")
        self.year13 = discord.utils.get(self.guild.roles, name = "Year 13")
        self.university = discord.utils.get(self.guild.roles, name = "University")
        


    @commands.command(name='close')
    @commands.has_role(829495730464882741) #Staff on modmail server
    async def close(self, ctx):
        '''Closes modmail thread'''
        if ctx.channel.category_id not in [829495730464882744, 832016200950218792]: #Inbox/Applications
            await ctx.send(f"You can not run that command in this category!")
            return
            
        file_name = f"{ctx.channel.name}.txt"
        with open(file_name, 'w+') as file:
            async for message in ctx.channel.history(oldest_first=True, limit=200):
                file.write(f"[{str(message.created_at)[:-7]}] [{message.author.name}]  {message.content}" + "\n")

        with open(file_name, "r") as file:
            user = self.guild.get_member(await get_id_from_thread(ctx.channel))
            if user == None:
                await ctx.message.reply("Unable to find user ID in channel.")
                return
            await self.mail_log.send(f"Mod mail thread with {user.name} ({user.id}) was closed by {ctx.author.name} ({ctx.author.id})", file=discord.File(file, f"{ctx.channel.name}.txt"))
        
        await ctx.channel.delete(reason=f"Closed by {ctx.author.name} ({ctx.author.id})")
        os.remove(file_name)



    @commands.command(name="role")
    @commands.has_role(829495730464882741) #Staff on modmail server
    async def role(self, ctx, role, action:typing.Optional[str]="add", member:typing.Optional[discord.Member]=None):
        
        if role not in ["8", "9", "10", "11", "12", "13", "university", "u"]:
            await ctx.send(f"Unkown role: `{role}`. Accepted roles: `8`, `9`, `10`, `11`, `12`, `13` or `university`/`u`.")
            return

        if member == None:
            user_id = await get_id_from_thread(ctx.channel)
            if user_id == None:
                await ctx.message.reply("Unable to find user ID in channel.")
                return
            member = self.guild.get_member(user_id)
            if member == None:
                await ctx.message.reply("Unable to fetch member data, are they in the server?.")
                return

        else:
            member = self.guild.get_member(member.id)

        role_name = f"Year {role}"
        if role == "8":
            role = self.year8
        elif role == "9":
            role = self.year9
        elif role == "10":
            role = self.year10
        elif role == "11":
            role = self.year11
        elif role == "12":
            role = self.year12
        elif role == "13":
           role = self.year13
        elif role in ["university", "u"]:
            role = self.university
            role_name = "University"

        if action.lower() in ["remove", "r"]:
            await member.remove_roles(role)
            await ctx.message.reply(f"Removed role `{role_name}` to {member.mention} (**{member.name}**, {member.id}).")
        elif action.lower() == "add":
            await member.add_roles(role)
            await ctx.message.reply(f"Added role `{role_name}` to {member.mention} (**{member.name}**, {member.id}).")
        else:
            await ctx.message.reply(f"Unkown action '`{action}`', available types: `remove`/`r` or `add`.")



    @commands.command(name="roles", aliases=["r"])
    @commands.has_role(829495730464882741) #Staff on modmail server
    async def roles(self, ctx, user:typing.Optional[discord.User]=None):
        if user == None:
            user_id = await get_id_from_thread(ctx.channel)
            if user_id == None:
                await ctx.message.reply("Unable to find user ID in channel.")
                return
        member = self.guild.get_member(user_id)
        if member == None:
            await ctx.message.reply("Unable to fetch member data, are they in the server?.")
            return

        roles = "`@" + "` `@".join([role.name for role in member.roles[1:]]) + "`"

        embed = full_embed(
            author_name=member.name, 
            author_icon=member.avatar_url,
            title = "Roles",
            description = roles)

        sent = await ctx.message.reply(embed=embed)
        await sent.add_reaction("️<:y9:879495112659447858>")
        await sent.add_reaction("️<:y10:879495112558792764>")
        await sent.add_reaction("️<:y11:879495112084836383>")
        await sent.add_reaction("️<:y12:879495112571371530>")
        await sent.add_reaction("️<:y13:879495112361652234>")

    @commands.command(name="id")
    @commands.has_role(829495730464882741) #Staff on modmail server
    async def id(self, ctx):
        if ctx.channel.category_id not in [829495730464882744, 832016200950218792]: #Inbox/Applications
            await ctx.send(f"You can not run that command in this category!")
            return

        user_id = await get_id_from_thread(ctx.channel)
        if user_id == None:
            await ctx.message.reply("Unable to find user ID in channel.")
            return

        await ctx.message.reply(user_id)



    @commands.command(name="controlpanel", aliases=["panel", "cp", "control"])
    @commands.has_role(829495730464882741) #Staff on modmail server
    async def controlpanel(self, ctx):
        if ctx.channel.category_id not in [829495730464882744, 832016200950218792]: #Inbox/Applications
            await ctx.send(f"You can not run that command in this category!")
            return
        
        embed = full_embed(
            title="Thread control panel",
            description="🆔 - User's ID \n🎖️ - View user's roles \nℹ️ - View user's info")

        sent = await ctx.message.reply(embed=embed)
        await sent.add_reaction("🆔")
        await sent.add_reaction("🎖️")
        await sent.add_reaction("ℹ️")
        



    @commands.command(name="user", aliases=["info"])
    @commands.has_role(829495730464882741) #Staff on modmail server
    async def userinfo(self, ctx, user:typing.Optional[discord.User]=None):
        if user == None:
            member = self.guild.get_member(await get_id_from_thread(ctx.channel))
            if member == None:
                await ctx.message.reply("Unable to find user ID in channel.")
                return
        else:
            member = self.guild.get_member(int(user.id))        

        created_difference = time_ago_readable(member.created_at)
        joined_difference = time_ago_readable(member.joined_at)

        roles = "`@" + "` `@".join([role.name for role in member.roles[1:]]) + "`"

        embed = full_embed(
            author_name=member.name, 
            author_icon=member.avatar_url,
            fields={
                "User Information":f"""Name: **{member.name}**
                ID: `{member.id}` 
                Created: **{created_difference}** (`{member.created_at.strftime('%B %d, %Y at %H:%M UTC')}`)
                Mention: {member.mention}""",
                "Member Information":f"""Joined: **{joined_difference} ago** (`{member.joined_at.strftime('%B %d, %Y at %H:%M UTC')}`)
                Roles: {roles}"""
            },
            fields_inline=False,
            blank=True)

        await ctx.message.reply(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != 804299895778443276: return #ModMail bot
        if message.channel.category_id not in [829495730464882744, 832016200950218792]: return #Inbox/Applications

        if message.content.startswith("ACCOUNT AGE "):
            await message.add_reaction("🆔")
            await message.add_reaction("🎖️")
            await message.add_reaction("ℹ️")




def setup(bot: commands.Bot):
    bot.add_cog(ModmailCommands(bot))
