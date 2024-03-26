import os

def check_matching_file(self, filename: str, folder: str) -> str | None:
  "Checks if exists a file that starts with the given name in the given folder"
  matches = [f for f in os.listdir(folder) if os.path.isfile(f) and f.startswith(filename)]
  if matches:
    return matches[0]
  else:
    return None