from app.config import config
from PIL import Image, ImageDraw, ImageOps
from app.domain.tier import Tier, TierNames
from app.domain.tierlist import TierList
from math import ceil
from app.helpers.text_fonts import app_fonts

class ImageComposer:
  def __init__(self, logger):
    self.logger = logger
    self.x_cursor = 0
    self.y_cursor = 0

  def itemize(self, image: Image, size: int):
    border_size = int(size * config.BORDER_RATIO)
    image_ratio = 1 - config.BORDER_RATIO
    image_size = int(size * image_ratio), int(size * image_ratio)
    img = image.resize(image_size, Image.Resampling.LANCZOS)
    img = img.quantize(colors=26)
    itemized = ImageOps.expand(img, border=border_size, fill='black')
    return itemized

  def get_tier_rows(self, tier: Tier):
    tier_rows = ceil(tier.item_count / config.TIERLIST_ITEM_PER_LINE_LIMIT)
    return tier_rows
  
  def compose_tierlist(self, tier_list: TierList) -> Image:
    items_per_line = min(config.TIERLIST_ITEM_PER_LINE_LIMIT, tier_list.max_item_count)
    self.logger.info(f'items per line {items_per_line}')
    item_size = int(config.TIERLIST_MAX_X_SIZE / (items_per_line+1))
    border_size = int(item_size * config.BORDER_RATIO)
    tier_imgs = []
    # --------- TITLE ---------
    if tier_list.title:
      title_font = app_fonts['TITLE']
      image = Image.new('RGBA', (config.TIERLIST_MAX_X_SIZE, item_size), (0,0,0))
      draw = ImageDraw.Draw(image)
      draw.text((15,15), tier_list.title, (100,100,100), font=title_font)
      tier_imgs.append(image)
    for tier in tier_list.tiers:
      x_cursor=0
      y_cursor=0
      tier_rows = self.get_tier_rows(tier)
      self.logger.info(f'TIER ROWS: {tier_rows}')
      
      new_tier_image = Image.new('RGBA', (config.TIERLIST_MAX_X_SIZE, int(item_size*tier_rows)), (0,0,0))
      grey_area = Image.new('RGB', (config.TIERLIST_MAX_X_SIZE - border_size - item_size, item_size*tier_rows - border_size), (20,20,20))
      new_tier_image.paste(grey_area, (item_size + border_size, border_size))
    
      tier_logo = self.itemize(tier.image, item_size)
      mid_point =  int((tier_rows-1)*(item_size/2))
      new_tier_image.paste(tier_logo, (0, mid_point))
      x_cursor += item_size
      
      for index, item in enumerate(tier.items):
        self.logger.info(f'NewItem {index, item, x_cursor, y_cursor}')
        if index != 0 and index % items_per_line == 0:
            self.logger.info(f'NewLine (Internal)')
            y_cursor += item_size
            x_cursor = item_size
        item_logo = self.itemize(item.image, item_size)
        new_tier_image.paste(item_logo, (x_cursor, y_cursor))
        x_cursor += item_size
        
      tier_imgs.append(new_tier_image)
      new_tier_image.save(f'generated/temp/tier_{tier.number}.png')

    full_height = sum([img.height for img in tier_imgs])
    
    full_image = Image.new('RGBA', (config.TIERLIST_MAX_X_SIZE + border_size, full_height + border_size), (0,0,0))
    y_cursor = 0
    for img in tier_imgs:
      full_image.paste(img, (0, y_cursor))
      y_cursor += img.height
  
    return full_image


  def text_to_tier_image(self, text: str) -> Image:
    image = Image.open('assets/text_template.png')
    draw = ImageDraw.Draw(image)
    mf = app_fonts['STANDART']
    draw.text((15,15), text, (0,0,0), font=mf)
    return image