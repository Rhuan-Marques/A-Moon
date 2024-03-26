from pydantic import BaseModel, field_validator, computed_field, ConfigDict, field_serializer, Field
from aenum import MultiValueEnum
from exceptions import TierListException, ImpossibleTierException
from PIL import Image
from app.domain.item import Item
from typing import Optional

class TierNames(MultiValueEnum):

  NONE = '?', -100
  SSS = 'SSS', -1
  SS = 'SS', 0
  S = 'S', 1
  A = 'A', 2
  B = 'B', 3
  C = 'C', 4
  D = 'D', 5
  F = 'F', 6
  FF = 'FF', 7
  NERD = 'NERD', 100
  
  def __str__(self):
    return self.value

  @property
  def number(self):
    return self.values[1]

  @classmethod
  def str_value_list(cls):
    return [item.value for item in cls]

class Tier(BaseModel):
  model_config = ConfigDict(arbitrary_types_allowed=True)
  buff: float = 0.0
  name: TierNames | str = TierNames.NONE
  number: int = Field(default=-100, validate_default=True)
  items: list[Item] = []
  
  @field_validator('name')
  @classmethod
  def validate_name(cls, v, values):
    v = v.value if isinstance(v, TierNames) else v
    if isinstance(v, str):
      values.data['buff'] = 0.1*v.count('-') - 0.1*v.count('+')
      raw_name = v.replace('+', '').replace('-', '').upper()
      tier_name =  TierNames.NONE if raw_name not in TierNames.str_value_list() else TierNames[raw_name] 
      return tier_name
    else:
      raise ImpossibleTierException(v)

  @field_validator('number')
  @classmethod
  def validate_number(cls, v, values):
    print(values.data)
    if 'name' not in values.data or values.data['name'] == TierNames.NONE:
      if isinstance(v, int):
        if v in [e.number for e in TierNames]:
            tier_name = TierNames(v)
            return v
        return TierNames.NONE.number
        
      else:
        raise ImpossibleTierException(v)
    else:
      return values.data['name'].number
    

  @computed_field
  def position(self) -> float:
    return self.number + self.buff

  @computed_field
  def image(self) -> Image:
    return Image.open(f'assets/tiers/tier_{self.number}.png')

  @computed_field
  def item_count(self) -> int:
    item_count = len(self.items)
    if item_count > 25:
      raise ValueError(f'Too many items in a tier {self.name}, cannot create image')
    elif item_count < 1:
      raise ValueError(f'No items in a tier {self.name}, cannot create image')
    return item_count

  @field_serializer('image')
  def serialize_image(self, v):
    return v.filename

  @field_serializer('name')
  def serialize_name(self, v):
    return v.value

  def __add__(self, other):
    if isinstance(other, Tier):
      self.items += other.items
    elif isinstance(other, Item):
      self.items.append(other)
    return self

  def __lt__ (self, other):
    return self.position < other.position