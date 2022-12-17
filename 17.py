from collections import namedtuple
import util

Position = namedtuple('Position', ['x', 'y'])


MOVE_LEFT = "<"
MOVE_RIGHT = ">"



def read_data():
  air_lines = util.read_lines("./17.data")

  shapes = []
  shape_lines = util.read_lines("./17-shapes.data")
  # read from bottom to top to increment y-pos while reading
  shape_lines = list(reversed(shape_lines))
  shape_lines.append("")   # easier to finish last shape
  cur_shape = set()
  
  cur_y = 0
  for line in shape_lines:
    if line == "":
      shapes.append(cur_shape)
      cur_shape = set()
      cur_y = 0
    else:
      for x in range(0, len(line)):
        w = line[x]
        if w == "#":
          cur_shape.add(Position(x,cur_y))
      cur_y += 1

  # top of file should be first shape
  shapes = list(reversed(shapes))
  return (air_lines[0], shapes)



def shape_translate(shape, delta):
  new_shape = set()
  for pos in shape:
    new_pos = Position(pos.x + delta.x, pos.y +delta.y)
    new_shape.add(new_pos)
  return new_shape

def get_shape_max_y(shape):
  max_y = None
  for pos in shape:
    if max_y == None:
      max_y = pos.y
    else:
      max_y = max(max_y, pos.y)
  return max_y

(air_pattern, shapes) = read_data()

chamber = set()
chamber_width = 7
shape_start_x = 2
shape_start_y_offset = 3
y_max = 0

# ground of chamber
for x in range(0, chamber_width+2):
  chamber.add(Position(x-1, -1))

# first move left/right
# then fall down  (rest, if no more down possible)

idx_air = 0
for n_shape in range(2022):
  idx_shape = n_shape % 5
  shape = shapes[idx_shape]
  idx_shape += 1
  
  shape_height = 1 +get_shape_max_y(shape)
  # add border left and right / full height of shape
  for dy in range(0, shape_height+shape_start_y_offset):
    chamber.add(Position(-1,y_max+dy))
    chamber.add(Position(chamber_width,y_max+dy))

  shape = shape_translate(shape, Position(shape_start_x, y_max+shape_start_y_offset))
  shape_falling = True
  while shape_falling:
    cur_air = air_pattern[idx_air]
    idx_air += 1
    idx_air = idx_air % len(air_pattern)
    new_shape = None
    if cur_air == MOVE_RIGHT:
      new_shape = shape_translate(shape, Position(1,0))
    elif cur_air == MOVE_LEFT:
      new_shape = shape_translate(shape, Position(-1,0))
    else:
      raise Exception(f'bad air type: {cur_air}')

    overlap = chamber.intersection(new_shape)
    if len(overlap) == 0:
      shape = new_shape

    # move down
    new_shape = shape_translate(shape, Position(0,-1))
    overlap = chamber.intersection(new_shape)
    if len(overlap) == 0:
      shape = new_shape
    else:
      print(f'stop shape {idx_shape}')
      for pos in shape:
        chamber.add(pos)
      shape_falling = False
      y_shape_max = get_shape_max_y(shape)
      y_max = max(y_max, y_shape_max+1)


print(f'y max: {y_max}')