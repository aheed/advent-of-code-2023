from enum import Enum
from dataclasses import dataclass
import utils

@dataclass(frozen=True)
class Instruction:
    direction: str
    distance: int
    dbg: int

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

def get_direction(n: int) -> str:
    match n:
        case 0:
            return "R"
        case 1:
            return "D"
        case 2:
            return "L"
        case 3:
            return "U"
        case _:
            assert(False)

def get_instruction(line: str) -> Instruction:
    parts = line.split(" ")
    return Instruction(direction=get_direction(int(parts[2][-2:-1])), dbg=int(parts[1]), distance=int(parts[2][2:-2], 16))

instructions = [get_instruction(line) for line in lines]
#print(instructions)


x=0
y=0
min_x = x
min_y = y
max_x = x
max_y = y
for instr in instructions:
    match instr.direction:
        case "R":
            x = x + instr.distance
        case "L":
            x = x - instr.distance
        case "D":
            y = y + instr.distance
        case "U":
            y = y - instr.distance
        case _:
            assert(False)
    min_x = min(x, min_x)
    max_x = max(x, max_x)
    min_y = min(y, min_y)
    max_y = max(y, max_y)

max_x = max_x - min_x
max_y = max_y - min_y

print(max_x, max_y)

def instruction_to_command(instructions: list[Instruction], index: int) -> int:
    
    match instructions[index].direction:
        case "R":
            match instructions[index-1].direction:
                case "D":
                    multiplier = -1
                case "U":
                    multiplier = 1
                case _:
                    assert(False)        
        case "L":
            match instructions[index-1].direction:
                case "D":
                    multiplier = 1
                case "U":
                    multiplier = -1
                case _:
                    assert(False)
        case "D":
            match instructions[index-1].direction:
                case "R":
                    multiplier = 1
                case "L":
                    multiplier = -1
                case _:
                    assert(False)
        case "U":
            match instructions[index-1].direction:
                case "R":
                    multiplier = -1
                case "L":
                    multiplier = 1
                case _:
                    assert(False)
        case _:
            assert(False)
    return instructions[index].distance * multiplier

commands = [instruction_to_command(instructions=instructions, index=index) for index in range(len(instructions))]
print(commands)

#############
"""
Rewrite reading of values (use the hex code)
Verify it's a loop
Convert to sequence of LR instructions instead of orientation

while not done:
    identify RR:
      reduce 0 and 2 by min(0 ,2)
      add 1 * min(0, 2) to total
    identify instructions with 0 distance
      -1 = -1 + 1
      remove 0 and 1

while True:
    identify LRR
      if not found
        break
      reduce 0 and 2 by min(0 ,2)
      add 1 * min(0, 2) to total

cases:
  0 < 2
  2 < 0
  -1 is L
  -1 is R
  3 is L
  3 is R

Assume LRR:
0 < 2
  -1 or 3 does not matter

2 > 0
  3 is L
    still works
  3 is R
    ?
"""