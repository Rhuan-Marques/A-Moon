
class AMoonException(Exception):
  code: str
  message: str
  def __init__(self, code, message):
    self.code = code
    self.message = message

class ImpossibleTierException(AMoonException):
  def __init__(self, tier: str):
    super().__init__("IMPOSSIBLE_TIER", f"The tier {tier} is impossible to achieve.")