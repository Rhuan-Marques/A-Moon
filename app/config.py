from pydantic_settings import BaseSettings
import os

class Config(BaseSettings):
  # These configurations should be automatically getting the values from env
  # But repl.it envs are weird, change it when changing the platform
  BOT_KEY: str = os.environ['MOON_SECRET_KEY']
  BOT_COMMAND_PREFIX: str = '<'
  TIERLIST_MAX_X_SIZE: int = 1920
  TIERLIST_MAX_Y_SIZE: int = 1080
  TIERLIST_ITEM_PER_LINE_LIMIT: int = 9
  BORDER_RATIO: float = 0.1
  MAX_RETRIES_DOWNLOAD_IMAGE: int = 5
  DEBUG_MODE: bool = False

config = Config()