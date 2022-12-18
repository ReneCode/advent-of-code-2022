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

def get_sides(positions):
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
  return sides

def is_inside(pos, cubes_set):
  (x,y,z) = pos
  return Position(x-1,y,z) in cubes_set and \
         Position(x+1,y,z) in cubes_set and \
         Position(x,y-1,z) in cubes_set and \
         Position(x,y+1,z) in cubes_set and \
         Position(x,y,z-1) in cubes_set and \
         Position(x,y,z+1) in cubes_set



sides = get_sides(positions)
print(f'part-1 sides: {sides}')

# part-2

min_x = None
min_y = None
min_z = None
max_x = None
max_y = None
max_z = None
for pos in positions:
  if min_x == None:
    min_x = pos.x
    max_x = pos.x
    min_y = pos.y
    max_y = pos.y
    min_z = pos.z
    max_z = pos.z
  else:
    min_x = min(min_x, pos.x)
    max_x = max(max_x, pos.x)
    min_y = min(min_y, pos.y)
    max_y = max(max_y, pos.y)
    min_z = min(min_z, pos.z)
    max_z = max(max_z, pos.z)

# use set to check existens quicker
cubes_set = set()
for pos in positions:
  cubes_set.add(pos)

air_holes = set()
for x in range(min_x, max_x):
  for y in range(min_y, max_y):
    for z in range(min_z, max_z):
      pos = Position(x,y,z)
      if pos in cubes_set:
        continue
      if is_inside(pos, cubes_set):
        air_holes.add(pos)



air_hole_sides = get_sides(air_holes)
print(f'part-2 air holes:{air_holes} sides:{air_hole_sides}')
print(f' => relevant sides: {sides - air_hole_sides}')
