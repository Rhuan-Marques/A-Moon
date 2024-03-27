import discord
from discord.ext import commands
import sys
from app.exceptions import AMoonException

class AMoon(commands.Bot):
  logger = logging.getLogger('discord')
  
  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

  async def on_command_error(self, ctx: commands.Context, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("I could not find member '{error.argument}'. Please try again")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"'{error.param.name}' is a required argument.")
    else:
        logger.info(f'Unexpected exception in command {ctx.command}:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

