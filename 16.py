import util

time_left = 30

time_to_move_room = 1
time_to_close_valve = 1

START_NAME  = "AA"


# total_pressure = time * rate

class Valve:
  def __init__(self, name, rate, other_valves):
    self.name = name
    self.rate = rate
    self.other_valves = other_valves


def get_data():
  valves = []
  lines = util.read_lines("./16.data")
  for line in lines:
    tok = line.split(" ")
    name = tok[1]
    rate = int(tok[4].split("=")[1].split(";")[0])
    others = []
    idx = 9
    while idx < len(tok):
      other = tok[idx].split(",")[0]
      others.append(other)
      idx += 1
    valve = Valve(name, rate, others)
    valves.append(valve)
  return valves


def get_touple_names(names):
  if len(names) < 2:
    raise Exception(f'get_double_targets not enough names')
  results = []
  for n1 in names:
    rest_names = [n for n in names if n != n1]
    for n2 in rest_names:
      results.append( (n1, n2))
  return results


def test_1():
  names = ['a','b','c']
  touple_names = get_touple_names(names)
  touple_names = [('a','b'),('a','c'),('b','a'),('b','c'),('c','a'),('c','b')]

class Path:
  def __init__(self, visited_names, target_names, time_left, pressure):
    self.visited_names = visited_names
    self.target_names = target_names
    self.pressure = pressure
    self.time_left = time_left
    self.finshed = False

  def get_current_name(self):
    return self.visited_names[-1]

IDX_ME = 0
IDX_ELEPHANT = 1


class MinutePath:
  def __init__(self, current_names, current_target_names, target_names, pressure, moving_times):
    self.current_names = current_names
    self.current_target_names = current_target_names
    self.target_names = target_names
    self.pressure = pressure
    self.moving_times = moving_times
    self.visited = []

class DoublePath:
  def __init__(self, visited_names, target_names, times_left, pressure):
    self.visited_names = visited_names
    self.target_names = target_names
    self.pressure = pressure
    self.times_left = times_left
    self.finshed = False

  def get_current_names(self):
    return [self.visited_names[0][-1],self.visited_names[1][-1]]
    
class WayFinder:
  def __init__(self, valves):
    self.valves = valves

  def get_valve(self, name):
    for valve in self.valves:
      if valve.name == name:
        return valve
    raise Exception(f'valve {name} not found')


  def calc_distance(self, v1_name, v2_name):
    # Dijstra
    que_names = [v1_name]
    distances = {v1_name:0}
    visited = set()
    while len(que_names) > 0:
      # get name from que with min distance
      cur_name = None
      min_dist = 999
      for name in que_names:
        if distances.get(name) != None and distances[name] < min_dist:
          min_dist = distances[name]
          cur_name = name
      
      cur = self.get_valve(cur_name)
      cur_distance = distances[cur_name]
      next_names = cur.other_valves
      for next_name in next_names:
        if not next_name in visited:
          if distances.get(next_name) == None  or distances[next_name] > (cur_distance+1):
            new_dist = cur_distance + 1
            if next_name == v2_name:
              return new_dist
            distances[next_name] = new_dist
            que_names.append(next_name)

      # remove from que
      que_names = [name for name in que_names if name != cur_name]
      visited.add(cur_name)
    return None

  def get_new_graph(self):
    rooms = [v for v in self.valves if v.rate > 0]

    # add first value
    start_valve = self.get_valve(START_NAME)
    rooms.append(start_valve)

    result = {}
    for idx_start in range(0, len(rooms)):
      start_name = rooms[idx_start].name
      distances = {}
      for idx_end in range(0, len(rooms)):
        if idx_start == idx_end:
          continue
        end_name = rooms[idx_end].name
        dist = self.calc_distance(start_name, end_name)
        distances[end_name] = dist
      result[start_name] = distances
    return result

  def calc_all_single_path(self, start_time_left):
    graph = self.get_new_graph()

    first_name = START_NAME
    target_names = [i for i in graph if i != first_name]

    path = Path([first_name], target_names, start_time_left, 0)
    all_path = [path]
    for path in all_path:
      if path.time_left <= 0:
        continue
      
      current_name = path.get_current_name()
      for target_name in path.target_names:
        rate = self.get_valve(target_name).rate
        way_cost = graph[current_name][target_name]
        pressure = (path.time_left - way_cost -1) * rate
        new_time_left = path.time_left - way_cost -1
        new_target_names = [name for name in path.target_names if name != target_name]
        new_visited_names = path.visited_names + [target_name]
        new_pressure = path.pressure + pressure 
        new_path = Path(new_visited_names, new_target_names, new_time_left, new_pressure)
        all_path.append(new_path)
  
    return all_path

  def calc_all_minute_path(self, start_time_left):
    graph = self.get_new_graph()
    first_name = START_NAME
    start_target_names = [i for i in graph if i != first_name]
    path = MinutePath([None, None], [first_name, first_name], start_target_names, 0, [0,0])
    all_path = [path]
    minutes_left = start_time_left
    while minutes_left > 0:
      next_all_path = []
      for path in all_path:
        if len(path.target_names) == 0:
          # path has finished
          next_all_path.append(path)
          continue
        if path.moving_times[IDX_ME] > 0 and path.moving_times[IDX_ELEPHANT] > 0:
          # still moving
          path.moving_times[IDX_ME] -= 1
          path.moving_times[IDX_ELEPHANT] -= 1
          next_all_path.append(path)

        else:
          # target reached
          # calc new pressure
          for idx in range(IDX_ME, IDX_ELEPHANT+1):
            if path.moving_times[idx] == 0:
              current_name = path.current_target_names[idx]
              if current_name in path.target_names:
                path.visited = path.visited + [current_name]
                # remove it from tagets
                path.target_names = [n for n in path.target_names if n != current_name]
                # calc pressure
                rate = self.get_valve(current_name).rate
                pressure = minutes_left * rate
                path.pressure += pressure
            
              if len(path.target_names) == 0:
                # finished
                next_all_path.append(path)
                continue

          if path.moving_times[IDX_ME] == 0 and path.moving_times[IDX_ELEPHANT] == 0:
            current_name_me = path.current_target_names[IDX_ME]
            current_name_elephant = path.current_target_names[IDX_ELEPHANT]
            for new_target_name_me in path.target_names:
              moving_time_me = graph[current_name_me][new_target_name_me]
              for new_target_name_elephant in path.target_names:
                moving_time_elephant = graph[current_name_elephant][new_target_name_elephant]
                new_path = MinutePath(
                    [current_name_me, current_name_elephant], 
                    [new_target_name_me, new_target_name_elephant], 
                    path.target_names, path.pressure, 
                    [moving_time_me, moving_time_elephant])
                next_all_path.append(new_path)

          elif path.moving_times[IDX_ME] == 0 and path.moving_times[IDX_ELEPHANT] > 0:
            current_name = path.current_target_names[IDX_ME]
            for new_target_name in path.target_names:
              moving_time = graph[current_name][new_target_name]
              new_path = MinutePath(
                  [current_name, path.current_names[IDX_ELEPHANT]], 
                  [new_target_name, path.current_target_names[IDX_ELEPHANT]], 
                  path.target_names, path.pressure, 
                  [moving_time, path.moving_times[IDX_ELEPHANT]-1])
              next_all_path.append(new_path)

          elif path.moving_times[IDX_ME] > 0 and path.moving_times[IDX_ELEPHANT] == 0:
            current_name = path.current_target_names[IDX_ELEPHANT]
            for new_target_name in path.target_names:
              moving_time = graph[current_name][new_target_name]
              new_path = MinutePath(
                  [path.current_names[IDX_ME], current_name], 
                  [path.current_target_names[IDX_ME], new_target_name], 
                  path.target_names, path.pressure, 
                  [path.moving_times[IDX_ME]-1, moving_time])
              next_all_path.append(new_path)
          else:
            raise Exception(f'ups')

      print(f'minutes left: {minutes_left} count path: {len(next_all_path)}')
      all_path = next_all_path
      minutes_left -= 1
    return all_path



  def calc_all_double_path(self, start_time_left):
    graph = self.get_new_graph()

    first_name = START_NAME
    target_names = [i for i in graph if i != first_name]

    path = DoublePath([[first_name], [first_name]], target_names, [start_time_left,start_time_left], 0)
    all_path = [path]
    for path in all_path:
      if path.times_left[0] <= 0 or path.times_left[1] <= 0:
        continue
      if len(path.target_names) == 0:
        continue

      names = path.get_current_names()
      double_targets = get_touple_names(path.target_names)
      new_target_names = None
      new_pressure = path.pressure

      for double_target in double_targets:
        new_time_left_list = []
        new_visited_names = []
        new_target_names = path.target_names
        for idx in range(2):
          target_name = double_target[idx]
          current_name = names[idx]
          rate = self.get_valve(target_name).rate
          way_cost = graph[current_name][target_name]
          pressure = (path.times_left[idx] - way_cost -1) * rate
          new_time_left = path.times_left[idx] - way_cost -1
          new_time_left_list.append(new_time_left)
          new_target_names = [name for name in new_target_names if name != target_name]
          new_pressure = new_pressure + pressure 
          new_visited_names.append( path.visited_names[idx] + [double_target[idx]] )
        new_path = DoublePath(new_visited_names,
                new_target_names, 
                new_time_left_list, 
                new_pressure)
        all_path.append(new_path)
  
    return all_path

def part_1():
  valves = get_data()
  way_finder = WayFinder(valves)
  all_path = way_finder.calc_all_single_path(30)
  pressures = sorted([p.pressure for p in all_path], reverse=True)        
  pressure = pressures[0]
  print(f'part-1 len: {len(all_path)} => pressure:{pressure}')

def part_2():
  valves = get_data()
  way_finder = WayFinder(valves)
  all_path = way_finder.calc_all_minute_path(26)
  pressures = sorted([p.pressure for p in all_path], reverse=True)        
  pressure = pressures[0]
  print(f'part-2 pressure:{pressure}')

part_2()