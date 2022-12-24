from collections import namedtuple
import util

Position = namedtuple("Position", ["x", "y"])

WIND_UP = "^"
WIND_RIGHT = ">"
WIND_LEFT = "<"
WIND_DOWN = "v"
TILE_FREE = "."


def get_data():
  lines = util.read_lines("./24-example.data")
  x_len = len(lines[0])
  y_len = len(lines)
  x = lines[0].index(TILE_FREE)
  start = Position(x,0)
  x = lines[y_len-1].index(TILE_FREE)
  end = Position(x, y_len-1)
  board = {}
  for y in range(1, y_len-1):
    for x in range(1, x_len-1):
      if lines[y][x] != TILE_FREE:
        pos = Position(x,y)
        board[pos] = [lines[y][x]] 
  bbox = util.BoundingBox()
  bbox.add_pos(1,1)
  bbox.add_pos(x_len-2, y_len-2)
  return (board, start, end, bbox)


def get_next_pos(cur_pos, wind, bbox):
  pos = None
  if wind == WIND_DOWN:
    pos = Position(cur_pos.x, cur_pos.y+1)
    if pos.y > bbox.max_y:
      pos = Position(pos.x, bbox.min_y)
  elif wind == WIND_UP:
    pos = Position(cur_pos.x, cur_pos.y-1)
    if pos.y < bbox.min_y:
      pos = Position(pos.x, bbox.max_y)
  elif wind == WIND_RIGHT:
    pos = Position(cur_pos.x+1, cur_pos.y)
    if pos.x > bbox.max_x:
      pos = Position(bbox.min_x, pos.y)
  elif wind == WIND_LEFT:
    pos = Position(cur_pos.x-1, cur_pos.y)
    if pos.x < bbox.min_x:
      pos = Position(bbox.max_x, pos.y)
  else:
    raise Exception("bad wind:" + wind)
  return pos

def get_next_board(board, bbox):
  new_board = {}
  for pos, winds in board.items():
    for wind in winds:
      new_pos = get_next_pos(pos, wind, bbox)
      if new_board.get(new_pos) != None:
        new_board[new_pos].append(wind)
      else:
        new_board[new_pos] = [wind]
  return new_board

def print_board(board, bbox, start, end, me):
  for y in range(0, bbox.max_y+2):
    line = ""
    for x in range(0, bbox.max_x+2):
      out = "."
      pos = Position(x,y)
      if pos == me:
        out = "E"
      elif pos == start or pos == end:
        out = "."
      elif not bbox.inside(x,y):
        out = "#"
      else:
        if board.get(pos) == None:
          out = "."
        else:
          winds = board[pos]
          if len(winds) == 1:
            out = winds[0]
          else:
            out = str(len(winds))
      line += out
    print(line)

def calc_next_free_positions(board, me, bbox):
  next_pos = [
    Position(me.x,me.y-1),
    Position(me.x,me.y+1),
    Position(me.x-1,me.y),
    Position(me.x+1,me.y)
  ]
  result = []
  for pos in next_pos:
    if bbox.inside(pos.x, pos.y):
      if board.get(pos) == None:
        result.append(pos)
  return result

(board, start, end, bbox) = get_data()
me = start
print('==== start ====')
print_board(board, bbox, start, end, me)
for minute in range(1, 9+1):
  board = get_next_board(board, bbox)
  next_free_positions = calc_next_free_positions(board, me, bbox)
  if len(next_free_positions) == 1:
    me = next_free_positions[0]
  print(f'==== Minute {minute} ====')
  print(next_free_positions)
  print_board(board, bbox, start, end, me)

# print(board, start, end)

