from pydantic import BaseModel, field_validator, computed_field
from app.domain.tier import Tier, TierNames
from typing import Optional

class TierList(BaseModel):
  tiers: list[Tier] = []
  title: Optional[str] = None

  def add_tier(self, tier: Tier):
    for stored_tier in self.tiers:
      if stored_tier.position == tier.position:
        stored_tier += tier
        return
    self.tiers.append(tier)

  @computed_field
  def tier_count(self) -> int:
    return len(self.tiers)

  @computed_field
  def max_item_count(self) -> int:
    return max(tier.item_count for tier in self.tiers)

  def finalize(self):
    self.tiers.sort()