from exceptions import TierListException, ImpossibleTierException
from app.domain.item import Item
from app.domain.tier import Tier, TierNames
from app.domain.tierlist import TierList
from app.services.image_downloader import ImageDownloaderServices
from app.services.image_composer import ImageComposer
from app.helpers.flavor_text import get_random_flavor_text
from app.helpers.clear_temp import clear_temp
import os
import logging
import discord
import sys
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
import uuid
import json

DEBUG_MODE = False
if DEBUG_MODE:
  logger = logging.getLogger()
  logger.addHandler(logging.StreamHandler(sys.stdout))
  logger.setLevel(logging.INFO)
else:
  logger = logging.getLogger('discord')
  logger.setLevel(logging.DEBUG)

intents = discord.Intents.default()
intents.message_content = True
bot_key = os.environ['MOON_SECRET_KEY']

client =  commands.Bot(command_prefix='<', intents=intents, help_command=None)

img_downloader = ImageDownloaderServices(logger)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para utilizar esse comando")
    else:
        raise error

@client.hybrid_command()
async def make_tier_list(ctx, full_msg: str):
  try:
    logger.info(f"Received command: {full_msg}")
    logger.info(f'*** Making tierlist ***')
    async with ctx.typing():
      current_tier_num=1
      tier_list = TierList()
      lines = full_msg.splitlines() if len(full_msg.splitlines()) > 1 else full_msg.split('/')
      logger.info('lines = ' + str(lines))
      for line in lines:
        if not line or line == '\n':
          logger.info('Empty line, skipping')
          continue
        if ':' in line:
          tier_name, line = line.split(':', 1)
          logger.info(f'Tier {tier_name}: {line}')
          logger.info(str(TierNames.str_value_list()))
          tier = Tier(name=tier_name)
    
        else:
          tier = Tier(number=current_tier_num)
          current_tier_num += 1
        for name in line.split(','):
          item = Item(name=name, image=img_downloader.get_image(name))
          tier += item
    
        logger.info(f'tier {tier.name}|{tier.position} has {tier.item_count} items')
        tier_list.add_tier(tier)

      tier_list.finalize()
      logger.info(f'**** COMPOSE ****')
      full_image = ImageComposer(logger).compose_tierlist(tier_list)
      full_image = full_image.quantize(colors=256)
      list_img_path = f'generated/lists/{uuid.uuid4()}.png'
      full_image.save(list_img_path)
      clear_temp()
      logger.info(f'***WE DID IT REDIT***')
      logger.info(json.dumps(tier_list.model_dump()))
      
    await ctx.send(get_random_flavor_text(), file=discord.File(list_img_path))

  except Exception as e:
    error_message = """*Uh oh, back to the lab again*,
*Oh no, back to the lab again,*
*We messed up, back to the lab again*
*Not again, back to the lab again*
  
(It seems like an error occured, try again or contact an A Moon administrator if the error persist)
    """
    logger.error(f'Error: {e}')
    clear_temp()
    await ctx.send(error_message)
    raise e
  
  
@client.command()
@commands.has_permissions(administrator=True)
async def sync(ctx):
  logger.info('Syncing commands')
  try:
      synced = await client.tree.sync()
      await ctx.send(f'Synced {len(synced)} commands')
  except Exception as e:
    logger.error('Sync exceptions:' + str(e))
    await ctx.send(f'ERROR: {e}')

if not DEBUG_MODE:
  client.run(bot_key)

  
else:
  from app.helpers.discord_bot_tester import ContextMock
  import asyncio

  loop = asyncio.get_event_loop()
  ctx = ContextMock(logger)
  loop.run_until_complete(make_tier_list(ctx, 'SSS: Potato, Aang/S: human, dog, cat, Discord logo/A: Dolphin, SmashBrosBall /D:StopSign'))
    
    