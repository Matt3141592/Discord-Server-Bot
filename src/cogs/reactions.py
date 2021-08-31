import discord, discord.utils, datetime, time
from discord.ext import commands
from helpers.embed import full_embed
from helpers.misc import get_id_from_thread, time_ago_readable

class Reactions(commands.Cog, name="Reaction listners"):
  
    def __init__(self, bot):
        self.bot = bot
        self.guild = self.bot.get_guild(781979349855371314)
        self.emoji_blacklist = ['💩', '🤓']
        self.year8 = discord.utils.get(self.guild.roles, name = "Year 8")
        self.year9 = discord.utils.get(self.guild.roles, name = "Year 9")
        self.year10 = discord.utils.get(self.guild.roles, name = "Year 10")
        self.year11 = discord.utils.get(self.guild.roles, name = "Year 11")
        self.year12 = discord.utils.get(self.guild.roles, name = "Year 12")
        self.year13 = discord.utils.get(self.guild.roles, name = "Year 13")
        self.university = discord.utils.get(self.guild.roles, name = "University")
        self.staff_role = discord.utils.get(self.guild.roles, name = "Staff")
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id: return # Reaction isn't added by the bot
        
        if payload.guild_id == 781979349855371314: # Public server
                          
            member = self.guild.get_member(payload.user_id)
            if self.staff_role in member.roles:  
                if payload.emoji.name == '⭕':
                    message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
                    response = await message.reply(f"<@{message.author.id}> All requests for papers belong in <#834883643104034877>")
                    
                    embed = full_embed(
                        title=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                        description=f"⭕ Used in <#{payload.channel_id}> by moderator {member.mention} (**{member.name}**, {member.id}) \n\nMessage from <@{message.author.id}> (**{message.author.name}**, {message.author.id}): \n```{message.content}``` \n{response.jump_url}")
                    mod_log = self.bot.get_channel(829407725908787300)
                    await mod_log.send(embed=embed)
                    await message.delete()

            elif payload.channel_id == 841041240425365545: #Remove inappropriate emojis from #share-your-results
                if payload.emoji.name in self.emoji_blacklist:
                    await message.remove_reaction(payload.emoji, member)
      
      
        elif payload.guild_id == 829495730464882738: #Modmail server
            if payload.emoji.name not in ["ℹ️", "🎖️", "🆔"]: return
            channel = self.bot.get_channel(payload.channel_id)
            user_id = await get_id_from_thread(channel)
            user = self.bot.get_user(user_id)
            member = self.guild.get_member(user_id)
            requester = self.guild.get_member(payload.user_id)
                        
            
            if payload.emoji.name in ["ℹ️", "🎖️"]:
                if payload.emoji.name == "ℹ️":
                    
                    created_difference = time_ago_readable(user.created_at)
                    
                    embed = full_embed(
                        author_name=user.name, 
                        author_icon=user.avatar_url,
                        fields={
                            "User Information":f"Name: **{user.name}** \nID: `{user.id}` \nCreated: **{created_difference}** (`{user.created_at.strftime('%B %d, %Y at %H:%M UTC')}`) \nMention: {user.mention}"},
                        fields_inline=False,
                        blank=True)
                    
                    if member != None: #account in server
                        joined_difference = time_ago_readable(member.joined_at)
                        roles = "`@" + "` `@".join([role.name for role in member.roles[1:]]) + "`"
                        embed.add_field(name="Member Information", value=f"Joined: **{joined_difference} ago** (`{member.joined_at.strftime('%B %d, %Y at %H:%M UTC')}`) \nRoles: {roles}", inline=False)


                elif payload.emoji.name == "🎖️":
                    if member == None:
                        await channel.send(f"{requester.mention} Member not found so unable to fetch roles.")
                        return
                    roles = "`@" + "` `@".join([role.name for role in member.roles[1:]]) + "`"
                    embed = full_embed(
                        author_name=member.name, 
                        author_icon=member.avatar_url,
                        title = "Roles",
                        description = roles)
                
                embed.set_footer(text=f"Requested by {requester.name} ({requester.id})")
                await channel.send(embed=embed)

            elif payload.emoji.name == "🆔": 
                await channel.send(user.id)
            
            elif payload.emoji.name in ["y8", "y9", "y10", "y11", "y12", "y13", "u"]:
                if payload.emoji.name == "y9":
                    await member.add_roles(self.year9)
                    await channel.send(f"Added role `Year 9` to {member.mention}({member.name}) requested by {requester.name} ({requester.id})")
                elif payload.emoji.name == "y10":
                    await member.add_roles(self.year10)
                    await channel.send(f"Added role `Year 10` to {member.mention}({member.name}) requested by {requester.name} ({requester.id})")
                elif payload.emoji.name == "y11":
                    await member.add_roles(self.year11)
                    await channel.send(f"Added role `Year 11` to {member.mention}({member.name}) requested by {requester.name} ({requester.id})")
                elif payload.emoji.name == "y12":
                    await member.add_roles(self.year12)
                    await channel.send(f"Added role `Year 12` to {member.mention}({member.name}) requested by {requester.name} ({requester.id})")
                elif payload.emoji.name == "y13":
                    await member.add_roles(self.year13)
                    await channel.send(f"Added role `Year 13` to {member.mention}({member.name}) requested by {requester.name} ({requester.id})")


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.user_id == self.bot.user.id: return # Reaction isn't added by the bot
        
        if payload.guild_id == 829495730464882738: #Modmail server
            channel = self.bot.get_channel(payload.channel_id)
            member = self.guild.get_member(await get_id_from_thread(channel))
            requester = self.guild.get_member(payload.user_id)
            
            if payload.emoji.name in ["y8", "y9", "y10", "y11", "y12", "y13", "u"]:
                if payload.emoji.name == "y9":
                    await member.remove_roles(self.year9)
                    await channel.send(f"Removed role `Year 9` from {member.mention}({member.name}) requested by {requester.name} ({requester.id})")
                elif payload.emoji.name == "y10":
                    await member.remove_roles(self.year10)
                    await channel.send(f"Removed role `Year 10` from {member.mention}({member.name}) requested by {requester.name} ({requester.id})")
                elif payload.emoji.name == "y11":
                    await member.remove_roles(self.year11)
                    await channel.send(f"Removed role `Year 11` from {member.mention}({member.name}) requested by {requester.name} ({requester.id})")
                elif payload.emoji.name == "y12":
                    await member.remove_roles(self.year12)
                    await channel.send(f"Removed role `Year 12` from {member.mention}({member.name}) requested by {requester.name} ({requester.id})")
                elif payload.emoji.name == "y13":
                    await member.remove_roles(self.year13)
                    await channel.send(f"Removed role `Year 13` from {member.mention}({member.name}) requested by {requester.name} ({requester.id})")


def setup(bot):
	bot.add_cog(Reactions(bot))
