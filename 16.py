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


class Path:
  def __init__(self, visited_names, target_names, time_left, pressure):
    self.visited_names = visited_names
    self.target_names = target_names
    self.pressure = pressure
    self.time_left = time_left
    self.finshed = False
    self.len_visited = 0

  def get_current_name(self):
    return self.visited_names[-1]

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

  def calc_all_path(self, start_time_left, also_partial_path = False):
    graph = self.get_new_graph()

    first_name = START_NAME
    target_names = [i for i in graph if i != first_name]

    path = Path([first_name], target_names, start_time_left, 0)
    all_path = [path]
    for path in all_path:
      if path.time_left <= 0:
        continue
      if not also_partial_path:
        if len(path.target_names) == 0:
          path.finshed = True
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
        if also_partial_path:
          new_partial_path = Path(new_visited_names, [], new_time_left, new_pressure)
          path.finshed = True
          all_path.append(new_partial_path)
  
    return all_path



valves = get_data()
way_finder = WayFinder(valves)
all_path = way_finder.calc_all_path(30)
finished_all_path = [p for p in all_path if p.finshed]
visited_names = finished_all_path[0].visited_names
visited_names.remove(START_NAME)
len_all_visited = len(visited_names)
pressures = sorted([p.pressure for p in all_path], reverse=True)        
pressure = pressures[0]

print(f'part-1 pressure:{pressure}')

all_path = way_finder.calc_all_path(26, True)
for path in all_path:
  path.visited_names = set(path.visited_names)
  path.visited_names.remove(START_NAME)
  path.len_visited = len(path.visited_names)

combined_pressure = 0
for i in range(len(all_path)):
  p1 = all_path[i]
  for j in range(i+1, len(all_path)):
    p2 = all_path[j]
    length = p1.len_visited + p2.len_visited
    if length != len_all_visited:
      continue
    v_both = p1.visited_names.intersection(p2.visited_names)
    if len(v_both) == 0:
      combined_pressure = max(combined_pressure, p1.pressure + p2.pressure)
pressure = combined_pressure

print(f'part-2 pressure:{pressure}')
