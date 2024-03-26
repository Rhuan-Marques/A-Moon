valid_extentions = ['.jpeg', '.jpg', '.png', '.webp']

def get_extention(path: str) -> str:
  extention = '.' + path.split('.')[-1].split('?')[0].lower()
  return extention if extention in valid_extentions else None
