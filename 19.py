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

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3

PRODUCTS = [ORE, CLAY, OBSIDIAN, GEODE]


class Blueprint:
  def __init__(self, costs):
    self.costs = costs
    self.max_needed = self.get_max_needed(costs)

  def get_max_needed(self, costs):
    max_needed = [0,0,0,0]
    for p in PRODUCTS:
      cost = costs[p]
      for prod in PRODUCTS:
        max_needed[p] = max(max_needed[p], costs[prod][p])
    return max_needed


class Factory:
  def __init__(self, robots, inventory):
    self.robots = robots.copy()
    self.inventory = inventory.copy()

  def collect(self):
    new_inventory = self.inventory.copy()
    for product in PRODUCTS:
      count = self.robots[product]
      if count > 0:
        new_inventory[product] += count
    return new_inventory

  def can_build_robot(self, blueprint, product):
    # no more robots needed
    if product != GEODE and self.robots[product] >= blueprint.max_needed[product]:
      return False

    cost = blueprint.costs[product]
    for p in PRODUCTS:
      if self.inventory[p] < cost[p]:
        return False
    return True

  def build_robot(self, blueprint, product):
    if not self.can_build_robot(blueprint, product):
      raise Exception(f'ups cant build robot {product}')

    # print(f'create {product}-robot')
    cost = blueprint.costs[product]
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

  def calc_minutes_to_build_robot(self, blueprint, product):
    costs = blueprint[product]
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
  lines = util.read_lines("./19.data")
  blueprints = []
  for line in lines:
    tok = line.split(" ")
    # ore
    ore_robot_cost = [int(tok[6]), 0, 0, 0]
    # ore
    clay_robot_cost = [int(tok[12]), 0, 0, 0]
    # ore, clay
    obsidian_robot_cost = [int(tok[18]), int(tok[21]), 0, 0]
    # ore, obsidian
    geode_robot_cost = [int(tok[27]), 0, int(tok[30]), 0]
    costs = [
        ore_robot_cost,
        clay_robot_cost,
        obsidian_robot_cost,
        geode_robot_cost
    ]
    blueprints.append(Blueprint(costs))
  return blueprints


def add_robot(robots, resource):
  new_robots = robots.copy()
  new_robots[resource] += 1
  return new_robots


def substract_resources(inventory, resources):
  new_inventory = inventory.copy()
  for product in PRODUCTS:
    count = resources[product]
    new_inventory[product] -= count
    if new_inventory[product] < 0:
      raise Exception(f'ups negative count of resource {product}')
  return new_inventory



def get_max_geode(blueprint):
  robots = [1,0,0,0]
  inventory = [0,0,0,0]
  first_factory = Factory(robots, inventory)
  factories = [first_factory]
  for minute in range(1, 24 + 1):
    print(f'\n== start Minute {minute} ==')
    next_factories = []
    for factory in factories:
      new_inventory = factory.collect()

      # robot = factory.calc_robot_to_build()

      if not factory.can_build_robot(blueprint, GEODE):
        # do nothing is one opertunity
        next_factory = Factory(factory.robots, new_inventory)
        next_factories.append(next_factory)

      # factory.calc_minutes_to_build_robot()

      for resouce in reversed(PRODUCTS):
        if factory.can_build_robot(blueprint, resouce):
          (robot, used_resources) = factory.build_robot(blueprint, resouce)
          next_inventory = substract_resources(new_inventory, used_resources)
          next_robots = add_robot(factory.robots, robot)
          next_factory = Factory(next_robots, next_inventory)
          next_factories.append(next_factory)

    # a = sorted([f.robots[GEODE] for f in next_factories])[]
    max_geode_robots = sorted([f.robots[GEODE] for f in next_factories])[-1]

    factories = [f for f in next_factories if f.robots[GEODE] >= max_geode_robots]
    print(f'finished minute:{minute} factories:{len(factories)} max_geode_robots:{max_geode_robots}')

  sort = sorted(factories, reverse=True, key=lambda f:f.inventory[GEODE])
  count_geode = sort[0].inventory[GEODE]
  return count_geode


# part-1
total = 0
blueprints = get_data()
nr = 0
for blueprint in blueprints:
  nr += 1
  geode = get_max_geode(blueprint)
  print(f'{nr} / {geode}')
  total += nr * geode
print(f'part-1 total:{total}')


# geode = get_max_geode(blueprints[1])
# print(f'{nr} / {geode}')


# max_needed = get_max_needed(blueprint)
