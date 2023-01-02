import util
"""
ore -> clay-collector
       clay -> obsidian-collector
               obsidian -> geode-collector
                           geode

at start you have one ore-collector

quality level of blueprint = id of blueprint * count of geodes

total = sum of all quality levels
"""

ORE = 'ORE'
CLAY = 'CLAY'
OBSIDIAN = 'OBSIDIAN'
GEODE = 'GEODE'

PRODUCTS = [ORE, CLAY, OBSIDIAN, GEODE]


class Factory:
  def __init__(self, robots, inventory, blueprint):
    self.robots = robots.copy()
    self.inventory = inventory.copy()
    self.blueprint = blueprint
    self.max_needed = self.calc_max_needed()

  def calc_max_needed(self):
    max_needed = {}
    for p in PRODUCTS:
      max_needed[p] = 0
    for _p, costs in self.blueprint.items():
      for p, need in costs.items():
        max_needed[p] = max(max_needed[p], need)
    return max_needed

  def collect(self):
    new_inventory = self.inventory.copy()
    for resource, count in self.robots.items():
      if count > 0:
        # print(f'collect {count} of {resource}')
        # one robot can produce one resource
        new_inventory[resource] += count
    return new_inventory

  def can_build_robot(self, product):
    # no more robots needed
    if product != GEODE and self.robots[product] >= self.max_needed[product]:
      return False

    cost = self.blueprint[product]
    for needed_resource, needed_count in cost.items():
      # needed_count = cost[needed_resource]
      if self.inventory[needed_resource] < needed_count:
        return False
    return True

  def build_robot(self, product):
    if not self.can_build_robot(product):
      raise Exception(f'ups cant build robot {product}')

    # print(f'create {product}-robot')
    cost = self.blueprint[product]
    return (product, cost)

  def calc_minutes_to_get_resources(self, resource, count):
    inv = self.inventory[resource]
    if inv >= count:
      return 0
    count_robots = self.robots[product]
    if count_robots == 0:
      # infinitive minutes to go
      return None
    need = count - inv
    minutes = need // count
    if need % count == 0:
      return minutes
    else:
      return minutes + 1

  def calc_minutes_to_build_robot(self, product):
    costs = self.blueprint[product]
    minutes = None
    critical_product = None
    for p, count in costs.items():
      m = self.calc_minutes_to_get_resources(p, count)
      if m == None:
        return (None, p)
      if minutes == None:
        critical_product = p
        minutes = m
      else:
        if m > minutes:
          critical_product = p
          minutes = m
    return (minutes, critical_product)

  def calc_robot(self, product):
    pass

  def calc_robot_to_build(self):
    if self.can_build_robot(GEODE):
      return GEODE

    if not self.can_build_robot(OBSIDIAN):
      pass

    (minutes, critical_product) = self.calc_minutes_to_build_robot(GEODE)
    if minutes == None:
      (minutes, critical_product) = self.calc_minutes_to_build_robot(critical_product)


def get_data():
  lines = util.read_lines("./19-example.data")
  blueprints = []
  for line in lines:
    tok = line.split(" ")
    # ore
    ore_robot_cost = {ORE: int(tok[6])}
    # ore
    clay_robot_cost = {ORE: int(tok[12])}
    # ore, clay
    obsidian_robot_cost = {ORE: int(tok[18]), CLAY: int(tok[21])}
    # ore, obsidian
    geode_robot_cost = {ORE: int(tok[27]), OBSIDIAN: int(tok[30])}
    costs = {
        ORE: ore_robot_cost,
        CLAY: clay_robot_cost,
        OBSIDIAN: obsidian_robot_cost,
        GEODE: geode_robot_cost
    }
    blueprints.append(costs)
  return blueprints


def add_robot(robots, resource):
  new_robots = robots.copy()
  new_robots[resource] += 1
  return new_robots


def substract_resources(inventory, resources):
  new_inventory = inventory.copy()
  for resource, count in resources.items():
    new_inventory[resource] -= count
    if new_inventory[resource] < 0:
      raise Exception(f'ups negative count of resource {resource}')
  return new_inventory



def get_max_geode(blueprint):
  robots = {ORE: 1, CLAY: 0, OBSIDIAN: 0, GEODE: 0}
  inventory = {ORE: 0, CLAY: 0, OBSIDIAN: 0, GEODE: 0}
  first_factory = Factory(robots, inventory, blueprint)
  factories = [first_factory]
  for minute in range(1, 24 + 1):
    print(f'\n== start Minute {minute} ==')
    next_factories = []
    for factory in factories:
      new_inventory = factory.collect()

      # robot = factory.calc_robot_to_build()

      if not factory.can_build_robot(GEODE):
        # do nothing is one opertunity
        next_factory = Factory(factory.robots, new_inventory, factory.blueprint)
        next_factories.append(next_factory)

      # factory.calc_minutes_to_build_robot()

      for resouce in reversed(PRODUCTS):
        if factory.can_build_robot(resouce):
        # (robot, used_resources) = factory.try_build_robot(resouce)
        # if robot != None:
          (robot, used_resources) = factory.build_robot(resouce)
          next_inventory = substract_resources(new_inventory, used_resources)
          next_robots = add_robot(factory.robots, robot)
          next_factory = Factory(next_robots, next_inventory, factory.blueprint)
          next_factories.append(next_factory)
          # print(f'build robot {robot}')
          break
    factories = next_factories
    print(f'finished minute:{minute} factories:{len(next_factories)}')

  sort = sorted(factories, reverse=True, key=lambda f:f.inventory[GEODE])
  count_geode = sort[0].inventory[GEODE]
  return count_geode


# part-1
blueprints = get_data()
nr = 0
# for blueprint in blueprints:
#   nr += 1
#   geode = get_max_geode(blueprint)
#   print(f'{nr} / {geode}')

geode = get_max_geode(blueprints[1])
print(f'{nr} / {geode}')


# max_needed = get_max_needed(blueprint)
