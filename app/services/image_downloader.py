from duckduckgo_search import DDGS
import requests
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from logging import Logger
import uuid
from app.helpers.get_extention import get_extention
from app.services.image_composer import ImageComposer
from app.config import config
import validators

ddgs = DDGS()

class ImageDownloaderServices:

  def __init__(self, logger: Logger):
    self.logger = logger

  def get_image(self, query: str) -> Image:
    extention = ''
    retries = 0
    while retries < config.MAX_RETRIES_DOWNLOAD_IMAGE:
      url = self.get_image_url(query, offset=retries)
      extention = get_extention(url)
      if not extention:
        self.logger.info(f'Invalid image has no extention')
        retries+=1
        continue
      try:
        self.logger.info(f'got url for {query}')
        bytes = self.get_image_bytes(url)
        self.logger.info(f'got bytes')
        filename = query.replace(' ', '') + '__'  + str(uuid.uuid4()) + get_extention(url)
        filepath = self.save_image(bytes, filename)
        self.logger.info(f'saved image to {filepath}')
    
        image = Image.open(filepath)
        self.logger.info(f'opened image')
        return image
      except UnidentifiedImageError as invalid_img:
        self.logger.error('Invalid image, could not load')
        retries+=1
        continue

    self.logger.error('Ow shit, we got a max retry')
    return ImageComposer(self.logger).text_to_image(query)

  def get_image_url(self, query: str, offset: int) -> str | None:
    "Returns the a single image url from duckduckgo search"
    if validators.url(query):
      return query
    search_results = ddgs.images(query, region='wt-wt', safesearch='off')       
    image_urls = [next(search_results).get("image") for _ in range(offset+1)]

    if image_urls[offset]:
      return image_urls[offset]
    else:
        raise Exception(f'No image found for query: {query}')

  def get_image_bytes(self, url: str) -> bytes | None:
    "Returns the image bytes from the url"
    response = requests.get(url)
    return BytesIO(response.content)

  def save_image(self, image_bytes: bytes, filename: str) -> None:
    "Saves the image bytes to a file"
    filepath = f'generated/temp/{filename}'
    with open(filepath, 'wb') as f:
        f.write(image_bytes.read())
    return filepath

    
