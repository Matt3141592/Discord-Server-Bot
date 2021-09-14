import os, discord, typing, pprint
from discord_slash import cog_ext, SlashContext, ComponentContext
from discord_slash.utils.manage_components import create_button, create_actionrow, create_select, create_select_option
from discord_slash.model import ButtonStyle
from discord.ext import commands
from helpers.embed import full_embed
from helpers.misc import time_ago_readable, get_id_from_thread

modmail_guild_id = [829495730464882738]

class ModmailCommands(commands.Cog, name='Modmail Commands'):
    """Commands to make modmail easier"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.mail_log = self.bot.get_channel(829495730644713486)
        

    # --------------------------------------------
    # Misc functions
    # --------------------------------------------
    
    async def id_function(self, ctx):
        user_id = await get_id_from_thread(ctx.channel)
        if user_id == None:
            await ctx.send("Unable to find user ID in channel.")
            return
        await ctx.send(user_id)
    
    async def operation(self, member, role_name):
        if discord.utils.get(self.bot.get_guild(781979349855371314).roles, name=role_name) in member.roles:
            return "remove"
        return "add"

    async def roles_message(self, member):
        embed = full_embed(
            author_name=member.name, 
            author_icon=member.avatar_url,
            title = "Roles",
            description = "`@" + "` `@".join([role.name for role in member.roles[1:]]) + "`")     
        
        year8_status = await self.operation(member, "Year 8")
        year9_status = await self.operation(member, "Year 9")
        year10_status = await self.operation(member, "Year 10")
        year11_status = await self.operation(member, "Year 11")
        year12_status = await self.operation(member, "Year 12")
        year13_status = await self.operation(member, "Year 13")
        university_status = await self.operation(member, "University")
        
        bio_status = await self.operation(member, "Biology mentor")
        chem_status = await self.operation(member, "Chemistry mentor")
        phys_status = await self.operation(member, "Physics mentor")
        comp_status = await self.operation(member, "Computer science mentor")
        psych_status = await self.operation(member, "Psychology mentor")
        maths_status = await self.operation(member, "Maths mentor")
        lit_status = await self.operation(member, "English literature mentor")
        lang_status = await self.operation(member, "English language mentor")
        french_status = await self.operation(member, "French mentor")
        spanish_status = await self.operation(member, "Spanish mentor")
        latin_status = await self.operation(member, "Latin mentor")
        german_status = await self.operation(member, "German mentor")
        welsh_status = await self.operation(member, "Welsh mentor")
        mandarin_status = await self.operation(member, "Mandarin mentor")
        arabic_status = await self.operation(member, "Arabic mentor")
        geog_status = await self.operation(member, "Geography mentor")
        busin_status = await self.operation(member, "Business mentor")
        hist_status = await self.operation(member, "History mentor")
        econ_status = await self.operation(member, "Economic mentor")
        relig_status = await self.operation(member, "Religious studies mentor")
        pe_status = await self.operation(member, "Physical Education mentor")

        dropdown = create_select(
            options = [
                create_select_option(year8_status, value=f"{year8_status} 8", emoji=discord.utils.get(self.bot.emojis, name="y8")),
                create_select_option(year9_status, value=f"{year9_status} 9", emoji=discord.utils.get(self.bot.emojis, name="y9")),
                create_select_option(year10_status, value=f"{year10_status} 10", emoji=discord.utils.get(self.bot.emojis, name="y10")),
                create_select_option(year11_status, value=f"{year11_status} 11", emoji=discord.utils.get(self.bot.emojis, name="y11")),
                create_select_option(year12_status, value=f"{year12_status} 12", emoji=discord.utils.get(self.bot.emojis, name="y12")),
                create_select_option(year13_status, value=f"{year13_status} 13", emoji=discord.utils.get(self.bot.emojis, name="y13")),
                create_select_option(university_status, value=f"{university_status} university", emoji=discord.utils.get(self.bot.emojis, name="uni"))],
            placeholder="Change user's roles",
            custom_id="role_select",
            max_values=1)
        return embed, dropdown
    
        dropdown2 = create_select(
            options = [
                create_select_option(bio_status, value=f"{bio_status} 8", emoji=discord.utils.get(self.bot.emojis, name="y8")),
                create_select_option(year8_status, value=f"{year8_status} 8", emoji=discord.utils.get(self.bot.emojis, name="y8")),
                create_select_option(year8_status, value=f"{year8_status} 8", emoji=discord.utils.get(self.bot.emojis, name="y8"))],
            placeholder="Change user's mentor roles",
            custom_id="mentor_select",
            max_values=1)
        return embed, dropdown2
                


    # --------------------------------------------
    # Functions used by commands and components
    # --------------------------------------------

    async def roles_function(self, ctx):
        member = self.bot.get_guild(781979349855371314).get_member(await get_id_from_thread(ctx.channel))
        if member == None:
            await ctx.reply("Unable to fetch member data, are they in the server?.")
            return      
        embed, dropdown = await self.roles_message(member)

        await ctx.reply(embed=embed, components=[create_actionrow(dropdown)])


    async def role_edit(self, ctx, role, action="add"):
        guild = self.bot.get_guild(781979349855371314)
        role_name = f"Year {role}"
        if role == "8":
            role = discord.utils.get(guild.roles, name = "Year 8")
        elif role == "9":
            role = discord.utils.get(guild.roles, name = "Year 9")
        elif role == "10":
            role = discord.utils.get(guild.roles, name = "Year 10")
        elif role == "11":
            role = discord.utils.get(guild.roles, name = "Year 11")
        elif role == "12":
            role = discord.utils.get(guild.roles, name = "Year 12")
        elif role == "13":
           role = discord.utils.get(guild.roles, name = "Year 13")
        elif role == "university":
            role = discord.utils.get(guild.roles, name = "University")
            role_name = "University"
    
        member = guild.get_member(await get_id_from_thread(ctx.channel))
        if action == "remove":
            await member.remove_roles(role)
            await ctx.send(f"Removed role `{role_name}` from {member.mention} (**{member.name}**, {member.id}).", delete_after=15)
        elif action == "add":
            await member.add_roles(role)
            await ctx.send(f"Added role `{role_name}` to {member.mention} (**{member.name}**, {member.id}).",delete_after=15)


    async def info_function(self, ctx):
        member = self.bot.get_guild(781979349855371314).get_member(await get_id_from_thread(ctx.channel))
        if member == None:
            await ctx.reply("Unable to find user ID in channel or fetch member data.")
            return
        
        created_difference = time_ago_readable(member.created_at)
        joined_difference = time_ago_readable(member.joined_at)
        roles = "`@" + "` `@".join([role.name for role in member.roles[1:]]) + "`"

        embed = full_embed(
            author_name=member.name, author_icon=member.avatar_url,
            fields={
                "User Information":f"Name: **{member.name}** \nID: `{member.id}` \nCreated: **{created_difference}** (`{member.created_at.strftime('%B %d, %Y at %H:%M UTC')}`) \nMention: {member.mention}",
                "Member Information":f"Joined: **{joined_difference} ago** (`{member.joined_at.strftime('%B %d, %Y at %H:%M UTC')}`) \nRoles: {roles}"
            },
            fields_inline=False,
            blank=True)

        await ctx.reply(embed=embed)


    # --------------------------------------------
    # Commands redirecting to function
    # --------------------------------------------
    
    @cog_ext.cog_slash(name="info", description="Closes and logs thread", guild_ids=modmail_guild_id)
    @commands.has_role(829495730464882741) #Staff on modmail server
    async def info_command(self, ctx:SlashContext):
        await self.info_function(ctx)   

    @cog_ext.cog_slash(name="id", description="Fetches ID of thread creator", guild_ids=modmail_guild_id)
    @commands.has_role(829495730464882741) #Staff on modmail server
    async def id_command(self, ctx:SlashContext):
        await self.id_function(ctx)
    
    @cog_ext.cog_slash(name="roles", description="Displays role of thread creator", guild_ids=modmail_guild_id)
    @commands.has_role(829495730464882741) #Staff on modmail server
    async def roles_command(self, ctx:SlashContext):
        await self.roles_function(ctx)
    
    @cog_ext.cog_component() # Receives selects in roles drop down
    async def role_select(self, ctx: ComponentContext):
        split_value = ctx.selected_options[0].split()
        await self.role_edit(ctx, role=split_value[1], action=split_value[0])

        if split_value[0] == "add": action = "added"
        else: action = "removed"
        content = ctx.origin_message.content + f"\n{ctx.author} {action} `{split_value[1]}`"
    
        member = self.bot.get_guild(781979349855371314).get_member(await get_id_from_thread(ctx.channel))
        embed, dropdown = await self.roles_message(member)
        
        await ctx.origin_message.edit(content=content, embed=embed, components=[create_actionrow(dropdown)])
 

    # --------------------------------------------
    # Control panel command and functions to receive button inputs
    # --------------------------------------------
    
    @cog_ext.cog_slash(name="controlpanel", description="Returns the threads' control panel", guild_ids=modmail_guild_id)
    @commands.has_role(829495730464882741) #Staff on modmail server
    async def controlpanel(self, ctx):
        if ctx.channel.category_id not in [829495730464882744, 832016200950218792]: #Inbox/Applications
            await ctx.reply(f"You can not run that command in this category!")
            return
        
        embed = full_embed(
            title="Thread user control panel")

        await ctx.reply(embed=embed, components=[create_actionrow(
            create_button(style=ButtonStyle.blue, label="ID", custom_id="id_button"), 
            create_button(style=ButtonStyle.blue, label="Roles", custom_id="roles_button"), 
            create_button(style=ButtonStyle.blue, label="Info", custom_id="info_button"))])

    @cog_ext.cog_component()
    async def id_button(self, ctx: ComponentContext):
        await self.id_function(ctx)
    @cog_ext.cog_component()
    async def roles_button(self, ctx: ComponentContext):
        await self.roles_function(ctx)
    @cog_ext.cog_component()
    async def info_button(self, ctx: ComponentContext):
        await self.info_function(ctx)

   
    # --------------------------------------------
    # Other commands
    # --------------------------------------------

    @cog_ext.cog_slash(name="close", description="Closes and logs thread", guild_ids=modmail_guild_id)
    @commands.has_role(829495730464882741) #Staff on modmail server
    async def close_command(self, ctx:SlashContext):
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



def setup(bot: commands.Bot):
    bot.add_cog(ModmailCommands(bot))
