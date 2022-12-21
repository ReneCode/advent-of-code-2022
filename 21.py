import util

"""
job:
  yell a specific number
  or
  yell the result of a math operation

  for math operation needed two other monkeys
"""

class Monkey:
  def __init__(self, name, nr, ops):
    self.name = name
    self.nr = nr 
    if nr == None:
      self.first_name = ops[0]
      self.operation = ops[1]
      self.second_name = ops[2]

  def __repr__(self):
    out = f"{self.name}:"
    if self.nr != None:
      return f"{out} {self.nr}"
    else:
      return f"{out} {self.first_name} {self.operation} {self.second_name}"


def get_data():
  lines = util.read_lines('./21.data')
  monkeys = {}
  for line in lines:
    tok = line.split(":")
    name = tok[0]
    tok = tok[1].strip().split((" "))
    nr = None
    if tok[0].isdecimal():
      nr = int(tok[0])
      monkey = Monkey(name, nr, None)
    else:
      first_name = tok[0]
      operation = tok[1]
      second_name = tok[2]
      monkey = Monkey(name, None, (first_name, operation, second_name))

    monkeys[name] = monkey
  return monkeys



def solve(monkeys, name):
  monkey = monkeys[name]

  if monkey.nr != None:
    return monkey.nr

  first_result = solve(monkeys, monkey.first_name)
  second_result = solve(monkeys, monkey.second_name)
  result = None
  if monkey.operation == "+":
    result = first_result + second_result
  elif monkey.operation == "-":
    result = first_result - second_result
  elif monkey.operation == "/":
    result = int(first_result / second_result)
  elif monkey.operation == "*":
    result = first_result * second_result
  else:
    raise Exception(f"ups, wrong operation {monkey.operation}")
  return result




monkeys = get_data()
# print (monkeys)

# root = monkeys["ptdq"]
# root.hello()


result = solve(monkeys, "root")
print(result)