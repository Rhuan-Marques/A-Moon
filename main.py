from app.exceptions import AMoonException, ImpossibleTierException
from app.domain.item import Item
from app.domain.tier import Tier, TierNames
from app.domain.tierlist import TierList
from app.bot import AMoon
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
from app.config import config
from PIL import ImageFont

logger = logging.getLogger('discord') if not config.DEBUG_MODE else logging.getLogger().addHandler(logging.StreamHandler(sys.stdout)).setLevel(logging.INFO)

intents = discord.Intents.default()
intents.message_content = True

bot = AMoon(logger=logger, command_prefix=config.BOT_COMMAND_PREFIX, intents=intents, help_command=None)

@bot.hybrid_command()
async def make_tier_list(ctx, full_msg: str):
  
  img_downloader = ImageDownloaderServices(logger)
  
  logger.info(f"Received command: {full_msg}")
  logger.info(f'*** Making tierlist ***')
  async with ctx.typing():
    current_tier_num=1
    tier_list = TierList()
    lines = full_msg.splitlines() if len(full_msg.splitlines()) > 1 else full_msg.split('/')
    logger.info('lines = ' + str(lines))
    for line in lines:
      line = line.strip()
      if not line or line == '\n':
        logger.info('Empty line, skipping')
        continue
      if ':' in line:
        tier_name, line = [part.strip() for part in line.split(':', 1)]
        if tier_name == "TITLE":
          logger.info(f'Setting tierlist title to {line}')
          tier_list.title = line
          continue
        logger.info(f'Tier {tier_name}: {line}')
        logger.info(str(TierNames.str_value_list()))
        tier = Tier(name=tier_name)
  
      else:
        tier = Tier(number=current_tier_num)
        current_tier_num += 1
      for name in [part.strip() for part in line.split(',')]:
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

@bot.command()
@commands.has_permissions(administrator=True)
async def sync(ctx):
  logger.info('Syncing commands')
  try:
      synced = await bot.tree.sync()
      await ctx.send(f'Synced {len(synced)} commands')
  except Exception as e:
    logger.error('Sync exceptions:' + str(e))
    await ctx.send(f'ERROR: {e}')

if not config.DEBUG_MODE:
  bot.run(config.BOT_KEY)

else:
  loop = asyncio.get_event_loop()
  ctx = ContextMock(logger)
  loop.run_until_complete(make_tier_list(ctx, 'SSS: Potato, Aang/S: human, dog, cat, Discord logo/A: Dolphin, SmashBrosBall /D:StopSign'))
    
    