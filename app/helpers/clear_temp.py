import os
import glob

def clear_temp():
  files = glob.glob('generated/temp/*')
  for f in files:
      os.remove(f)