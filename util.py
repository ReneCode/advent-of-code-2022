
# read file into line array

from collections import namedtuple

def read_lines(filename, strip = True):
  with open(filename) as f:
      lines = f.readlines()
      lines = [l.strip('\n') for l in lines]
      if not strip:
        return lines
      lines = [l.strip() for l in lines]
      return lines

def signum(x):
  if x > 0:
    return 1
  elif x < 0:
    return -1
  else:
    return 0

Position = namedtuple('Position', ['x', 'y'])


class BoundingBox:
  def __init__(self):
    self.min_x = None
    self.max_x = None
    self.min_y = None
    self.max_y = None

  def __repr__(self):
    return f'{self.min_x},{self.min_y} / {self.max_x},{self.max_y}'

  def add_pos(self, x,y):
    if self.min_x == None:
      self.min_x = x
      self.max_x = x
      self.min_y = y
      self.max_y = y
    else:
      self.min_x = min(self.min_x, x)
      self.max_x = max(self.max_x, x)
      self.min_y = min(self.min_y, y)
      self.max_y = max(self.max_y, y)

