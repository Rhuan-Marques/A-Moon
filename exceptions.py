class TierListException(Exception):
  code: str
  message: str
  def __init__(self, code, message):
    self.code = code
    self.message = message

class ImpossibleTierException(TierListException):
  def __init__(self, tier):
    super().__init__("IMPOSSIBLE_TIER", "The tier you entered is impossible to achieve.")