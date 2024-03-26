import random

flavor_text = [
  "This one is good",
  "You WONT BELIEVE these takes (2019, NO VIRUS)",
  "Do not trust the third tier",
  "Honestly, what is this guy thinking?",
  "This is definetly a tierlist",
  "Bruh"
]

def get_random_flavor_text() -> str:
  return random.choice(flavor_text)