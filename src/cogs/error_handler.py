import discord
from discord.ext import commands
from helpers.embed import full_embed
from config import prefix



class ErrorHandler(commands.Cog):
    """Error handler"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.CommandNotFound):
            message = "Unkown command."
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f"Missing required argument: `{error.param}`. To view full command user `{prefix[0]}help <command>`."
        elif isinstance(error, commands.MissingPermissions):
            message = "You are missing the required permission(s) for this command."
        elif isinstance(error, commands.UserInputError):
            message = "There was an issue with your input, check your input and try again."
        else:
            message = "Unknown error occurred"
            raise error


        embed = full_embed(
            title="Error raised",
            description=message,
            colour=discord.Color.red()
        )
        await ctx.send(embed=embed)



def setup(bot: commands.Bot):
    bot.add_cog(ErrorHandler(bot))
