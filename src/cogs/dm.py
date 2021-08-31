import discord.utils
from discord.ext import commands


class DMs(commands.Cog):
    """Watching and responding to DMs"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.guild = self.bot.get_guild(781979349855371314)
        self.dmlog_channel = self.bot.get_channel(877335550296752138)
        
        self.roles = []
        self.year8 = discord.utils.get(self.guild.roles, name = "Year 8")
        self.year9 = discord.utils.get(self.guild.roles, name = "Year 9")
        self.year10 = discord.utils.get(self.guild.roles, name = "Year 10")
        self.year11 = discord.utils.get(self.guild.roles, name = "Year 11")
        self.year12 = discord.utils.get(self.guild.roles, name = "Year 12")
        self.year13 = discord.utils.get(self.guild.roles, name = "Year 13")
        self.university = discord.utils.get(self.guild.roles, name = "University")
        self.roles.append(self.year8)
        self.roles.append(self.year9)
        self.roles.append(self.year10)
        self.roles.append(self.year11)
        self.roles.append(self.year12)
        self.roles.append(self.year13)
        self.roles.append(self.university)

    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        if not message.guild: #If the message isn't in a server
            await self.dmlog_channel.send(f"{message.author.mention} (**{message.author.name}**, {message.author.id}): ```{message.content}"[:1990] + "```")

            if message.content in ["8", "9", "10", "11", "12", "13", "university"]:
                
                member = self.guild.get_member(message.author.id)
                for role in self.roles:
                    if role in member.roles:
                        await member.remove_roles(role)

                if message.content == "8":
                    await member.add_roles(self.year8)
                    role_name = "Year 8"
                elif message.content == "9":
                    await member.add_roles(self.year9)
                    role_name = "Year 9"
                elif message.content == "10":
                    await member.add_roles(self.year10)
                    role_name = "Year 10"
                elif message.content == "11":
                    await member.add_roles(self.year11)
                    role_name = "Year 11"
                elif message.content == "12":
                    await member.add_roles(self.year12)
                    role_name = "Year 12"
                elif message.content == "13":
                    await member.add_roles(self.year13)
                    role_name = "Year 13"
                elif message.content == "university":
                    await member.add_roles(self.university)
                    role_name = "University"

                await message.reply(f"Added role `{role_name}`.")
                await self.dmlog_channel.send(f"Given role `{role_name}` to {message.author.mention} (**{message.author.name}**, {message.author.id})")
            else:
                await message.channel.send("**Do you want to apply a year group role?** \n\nIf so reply with one of the following `8`, `9`, `10`, `11`, `12`, `13` or `university`.")




def setup(bot: commands.Bot):
    bot.add_cog(DMs(bot))
