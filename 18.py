from collections import namedtuple
import util

Position = namedtuple("Position", ['x','y','z'])


def get_data():
  lines = util.read_lines("./18.data")
  positions = []
  for line in lines:
    tok = line.split(",")
    pos = Position(int(tok[0]), int(tok[1]), int(tok[2]))
    positions.append(pos)
  return positions

def has_common_surface(a, b):
  if a.x == b.x and a.y == b.y and abs(a.z - b.z) == 1:
    return True
  if a.x == b.x and abs(a.y - b.y) == 1 and a.z == b.z:
    return True
  if abs(a.x - b.x) == 1 and a.y == b.y and a.z == b.z:
    return True

  return False

positions = get_data()
tested = []

sides = None
for pos in positions:
  if sides == None:
    tested.append(pos)
    sides = 6
  else:
    sides += 6
    for other in tested:
      if has_common_surface(pos, other):
        sides -= 2
    tested.append(pos)

print(f'part-1 sides: {sides}')



# class Cube:
#   def __init__(self, pos):
#     # pos is bottom, left, front verticie
#     # cube expans to top, right, back (1,1,1)
#     self.pos = pos

#   def has_common_surface(self, other):
#     if self.pos.x == other.pos
