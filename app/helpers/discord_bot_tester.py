class ContextMock:
  def __init__(self, logger):
    self.logger = logger
    
  async def send(self, msg: str, **kwargs):
    self.logger.info(f'--Send: {msg}')
  