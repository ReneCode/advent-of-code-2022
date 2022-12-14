from collections import namedtuple
import util

Position = namedtuple('Position', ['x', 'y'])

TILE_ROCK = "#"
TILE_SAND = "o"
TILE_AIR = "."


def pos_down(pos):
  return Position(pos.x, pos.y+1)

def pos_down_left(pos):
  return Position(pos.x-1, pos.y+1)

def pos_down_right(pos):
  return Position(pos.x+1, pos.y+1)

class Board:
  def __init__(self):
    self.positions = {}
    self.max_y = None

  def add_rock(self, pos):
    self.positions[pos] = TILE_ROCK

  def add_sand(self, pos):
    self.positions[pos] = TILE_SAND

  def calc_border(self):
    max_y = None
    for pos in self.positions:
      if max_y == None:
        max_y = pos.y
      else:
        max_y = max(max_y, pos.y)
    self.max_y = max_y

  def get_tile(self, pos):
    tile = self.positions.get(pos)
    if tile == None:
      return TILE_AIR
    else:
      return tile

  def is_blocked(self, pos):
    tile = self.get_tile(pos)
    return tile == TILE_ROCK or tile == TILE_SAND

  def pour_sand(self, pos):
    while pos.y < (self.max_y +1):
      new_pos = pos_down(pos)
      if self.is_blocked(new_pos):
        new_pos = pos_down_left(pos)
        if self.is_blocked(new_pos):
          new_pos = pos_down_right(pos)
          if self.is_blocked(new_pos):
            # sand comes to rest
            self.add_sand(pos)
            return True
          else:
            pos = new_pos
        else:
          pos = new_pos
      else:
        pos = new_pos

    # sand falls out of frame
    return False

def get_all_positions(p1, p2):
  # get all position between p1 and p2 exclusive p1
  dx = util.signum(p2.x - p1.x)
  dy = util.signum(p2.y - p1.y)
  pos = p1
  positions = []
  while pos != p2:
    pos = Position(pos.x + dx, pos.y + dy)
    positions.append(pos)
  return positions

def get_data():
  lines = util.read_lines('./14.data')
  board = Board()
  for line in lines:
    token = line.split("->")
    last_pos = None
    for tok in token:
      [x,y] = tok.split(",")
      x = int(x)
      y = int(y)
      pos = Position(x,y)
      if last_pos == None:
        last_pos = pos
        board.add_rock(pos)
      else:
        # draw line from last_pos to pos
        line_positions = get_all_positions(last_pos, pos)
        for line_pos in line_positions:
          board.add_rock(line_pos)
        last_pos = pos
  return board


TYPE_SAND = "o"
TYPE_ROCK = "#"

puring_pos = Position(500,0)

board = get_data()
board.calc_border()
total_sand = 0
while True:
  ok = board.pour_sand(puring_pos)
  if ok:
    total_sand += 1
  else:
    break

print(f'total_sand: {total_sand}')