from PIL import Image, ImageFont
from enum import Enum

app_fonts = {
  'STANDART': ImageFont.truetype('assets/colvetica.otf', 200),
  'TITLE': ImageFont.truetype('assets/colvetica.otf', 200)
}


def split_line_equaly(text: str, splits: int) -> list[str]:
  "Spits a line on ' ' in parts with similar lenghts"
  text_size = len(text)
  split_pos = {}
  for i in range(text_size):
    for split in range(splits) if split not in split_pos.keys():
      cursor = (text/splits) * (split+1) + i
      if text[cursor] == ' ':
        split_pos[split] = cursor
      cursor = (text/splits) * (split+1) - i
      if text[cursor] == ' ':
        split_pos[split] = cursor
  return [text[split_pos[split]:split_pos[split+1] for split in split_pos.values()[:-1]]

def get_dinamic_font(image_size: (int, int), text: str):
"""
Create a Pillow Font so that the text stays inside an image with the given sizes.
If the size of the font gets small enough so that 2 lines can be placed inside the image size,
it should split the text into two lines (if it has any space) to make it fit better.

:param image_size: A tuple of (width, height) for the image size.
:param text: The text to fit within the image.
:return: A tuple of the Pillow Font object and the possibly modified text (split into two lines if applicable).
"""

# Initial font size and font path (using a common font type)
font = ImageFont.truetype('assets/colvetica.otf', 500)

# Create a temporary image to get text size
temp_image = Image.new('RGB', image_size)
draw = ImageDraw.Draw(temp_image)

lines = 1;
# Decrease font size until the text fits the image width or can be split into two lines
while font_size > 0:
    # Check if text can be split

  if text.count(' ') > lines and font_size <= image_size[1] / lines+1:
    text_lines = split_line_equaly(text, lines)
    w1, h1 = draw.textsize(line1, font=font)
    w2, h2 = draw.textsize(line2, font=font)
    if max(w1, w2) <= image_size[0] and (h1 + h2) <= image_size[1]:
        text = line1 + '\n' + line2
        break

    # Measure text size with current font size
    w, h = draw.textsize(text, font=font)
    if w <= image_size[0] and h <= image_size[1]:
        break  # The text fits, stop adjusting the font size

    # Reduce font size and update font
    font_size -= max(5, font_size/20)
    font = ImageFont.truetype(font_path, font_size)

return font, text


