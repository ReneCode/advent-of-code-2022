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

def get_data():
  lines = util.read_lines("./19-example.data")
  blueprints = []
  for line in lines:
    tok = line.split(" ")
    # ore
    ore_robot_cost = {ORE:int(tok[6])}
    # ore
    clay_robot_cost = {ORE:int(tok[12])}
    # ore, clay
    obsidian_robot_cost = {ORE:int(tok[18]), CLAY:int(tok[21])}
    # ore, obsidian
    geode_robot_cost = {ORE: int(tok[27]), OBSIDIAN: int(tok[30])}
    costs = {ORE: ore_robot_cost, CLAY:clay_robot_cost, OBSIDIAN:obsidian_robot_cost, GEODE:geode_robot_cost}
    blueprints.append(costs)
  return blueprints



def procuce_by_robots(robots):
  result = {}
  for product in PRODUCTS:
    if robots.get(product) != None:
      robot_count = robots[product]
      result[product] = robot_count
  return result
    
def add_products(inventory, add_products):
  new_inventory = inventory.copy()
  for product in add_products:
    new_inventory[product] += add_products[product]
  return new_inventory

def add_robots(robots, add_robots):
  new_robots = robots.copy()
  for robot in add_robots:
    new_robots[robot] += add_robots[robot]
  return new_robots

def enough_products(inventory, cost):
  for needed_product in cost:
    needed_count = cost[needed_product]
    count = inventory.get(needed_product)
    if count < needed_count:
      return False
  return True

def build_robots(inventory, blueprint, cur_robots, max_needed):
  new_inventory = inventory.copy()
  new_robots = {}
  for product in PRODUCTS:
    if product != PRODUCTS[-1] and max_needed[product] <= cur_robots[product]:
      # no more robots for this product needed
      continue

    cost = blueprint.get(product)
    if cost == None:
      continue
    # check if all products are there - in the inventory
    if enough_products(new_inventory, cost):
      print(f'build {product}-robot')
      for needed_product in cost:
        count = cost[needed_product]
        new_inventory[needed_product] -= count
      new_robots.update({product:1})
  return (new_inventory, new_robots)

def get_max_needed(blueprint):
  
  max_needed = {}
  for product in PRODUCTS:
    max_needed[product] = 0
  
  for product in blueprint:
    costs = blueprint[product]
    for p in costs:
      product_cost = costs[p]
      max_needed[p] = max(max_needed[p], product_cost)
  return max_needed

# part-1
blueprints = get_data()
blueprint = blueprints[0]

robots = {ORE:1, CLAY:0, OBSIDIAN: 0, GEODE: 0}
inventory = {ORE:0, CLAY: 0, OBSIDIAN:0, GEODE:0}
max_needed = get_max_needed(blueprint)

for minute in range(1, 24+1):
  print(f'\n== start Minute {minute} ==')
  (new_inventory, created_robots) = build_robots(inventory, blueprint, robots, max_needed)
  inventory = new_inventory
  created_products = procuce_by_robots(robots)
  robots = add_robots(robots, created_robots)
  inventory = add_products(inventory, created_products)
  print(f'finished minute:{minute} inventory:{inventory} robots:{robots}')
