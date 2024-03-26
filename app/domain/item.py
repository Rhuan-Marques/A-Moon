from pydantic import BaseModel, field_validator, ConfigDict, field_serializer, SkipValidation
from PIL.Image import Image
from typing import Optional

class Item(BaseModel):
  model_config = ConfigDict(arbitrary_types_allowed=True)
  name: str
  image: Optional[Image] = None

  @field_serializer('image')
  def serialize_item(self, v):
    return v.filename if isinstance(v, Image) else 'None'