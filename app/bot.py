import discord
from discord.ext import commands
import sys
from app.exceptions import AMoonException
import logging
from logging import Logger
from app.config import config

class AMoon(commands.Bot):
  
  def __init__(self, logger: Logger, *args, **kwargs):
    self.logger = logger
    super().__init__(*args, **kwargs)

  def run(self, token: str, reconnect: bool = True):
    if not config.DEBUG_MODE:
      super().run(token, reconnect=reconnect)
    else:
      self.logger.info('DEBUG MODE INITIATED')
      # instantiate mock bot here

  async def on_ready(self):
    self.logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
    self.logger.info('------')
    
  
  async def on_command_error(self, ctx: commands.Context, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send(f'I could not find member {error.argument}. Please try again')
    elif isinstance(error, commands.MissingRequiredArgument):
      await ctx.send(f'{error.param.name} is a required argument.')
    else:
      await ctx.send("""
*Uh oh, back to the lab again*,
*Oh no, back to the lab again,*
*We messed up, back to the lab again*
*Not again, back to the lab again*

(It seems like an error occured, try again or contact an A Moon administrator if the error persist)
      """)
      self.logger.error(f'Unexpected exception in command {ctx.command}:')
      self.logger.error(f'{error}')