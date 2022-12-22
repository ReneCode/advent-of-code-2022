from collections import namedtuple
import util

Position = namedtuple("Position", ['x','y'])

TILE_FREE = "."
TILE_WALL = "#"
TILE_OUT = " "


DIR_RIGHT = 0
DIR_DOWN = 1
DIR_LEFT = 2
DIR_UP = 3

POS_DELTA = {
  DIR_UP:    (0,-1),
  DIR_RIGHT: (1,0),
  DIR_DOWN:  (0,1),
  DIR_LEFT:  (-1,0)
}


def get_data():
  lines = util.read_lines("./22.data", False)
  board = []
  commands = ""
  read_board = True
  max_len = 0
  for line in lines:
    if line.strip() == "":
      read_board = False
      continue
    if read_board:
      max_len = max(max_len, len(line))
      board.append(line)
    else:
      commands = []
      snr = ""
      for c in line:
        if c.isdecimal():
          snr += c
        else:
          commands.append(("MOVE", int(snr)))
          snr = ""
          commands.append(("TURN", c))
      commands.append(("MOVE", int(snr)))

  next_board = []
  for line in board:
    if len(line) < max_len:
      line += TILE_OUT * (max_len - len(line))
    next_board.append(line)
  return (next_board, commands)

def get_start_pos(board):
  line = board[0]
  for x in range(len(line)):
    if line[x] == TILE_FREE:
      return Position(x,0)
  raise Exception(f'no start position found')


def turn(direction, turn):
  if turn == "R":
    return (direction +1) % 4
  elif turn == "L":
    return (direction -1) % 4
  raise Exception(f'bad turn: {turn}')


def get_next_pos(pos, direction):
  delta = POS_DELTA[direction]
  return Position(pos.x + delta[0], pos.y + delta[1])

def adjust_pos(board, pos, direction):
  len_y = len(board)
  outside = pos.y >= len_y or \
            pos.y < 0 or \
            pos.x >= len(board[pos.y]) or \
            pos.x < 0 or \
            board[pos.y][pos.x] == TILE_OUT
  if outside and direction == DIR_UP:
    for y in reversed(range(len_y)):
      if board[y][pos.x] != TILE_OUT:
        return Position(pos.x,y)
    raise Exception(f'ups a')
  if outside and direction == DIR_DOWN:
    for y in range(len_y):
      if board[y][pos.x] != TILE_OUT:
        return Position(pos.x,y)
    raise Exception(f'ups b')
  if outside and direction == DIR_LEFT:
    for x in reversed(range(len(board[pos.y]))):
      if board[pos.y][x] != TILE_OUT:
        return Position(x, pos.y)
    raise Exception(f'ups c')
  if outside and direction == DIR_RIGHT:
    for x in range(len(board[pos.y])):
      if board[pos.y][x] != TILE_OUT:
        return Position(x, pos.y)
    raise Exception(f'ups d')
  return pos


def move(board, count, pos, direction):
  for i in range(count):
    next_pos = get_next_pos(pos, direction)
    next_pos = adjust_pos(board, next_pos, direction)
    new_tile = board[next_pos.y][next_pos.x]
    if new_tile == TILE_WALL:
      return pos
    # valid move      
    pos = next_pos

  return pos

(board, commands) = get_data()
pos = get_start_pos(board)
direction = DIR_RIGHT
print(f'start: {pos} {direction}')
nr = 0
for cmd in commands:
  if nr == 10:
    a = 42
  nr += 1
  if cmd[0] == "MOVE":
    pos = move(board, cmd[1], pos, direction)
  elif cmd[0] == "TURN":
    direction = turn(direction, cmd[1])
  else:
    raise Exception(f'bad cmd: {cmd[0]}')
  print(f'after {nr} {cmd}: {pos} {direction}')

result_col = pos.x +1
result_row = pos.y +1
result = 1000 * result_row + 4 * result_col + direction
print(f'part-1 result:{result}')
  