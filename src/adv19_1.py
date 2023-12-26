import re
from dataclasses import dataclass
import utils

@dataclass(frozen=True)
class Rule:
    param: str
    operation: str # > (greater than), < (less than), u (unconditional)
    value: int
    action: str

@dataclass(frozen=True)
class Workflow:
    name: str
    rules: list[Rule]


with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

first_part_index = lines.index("")
workflow_lines = lines[:first_part_index]
part_lines = lines[first_part_index+1:]

def str_to_rule(rstr: str) -> Rule:
    if not ":" in rstr:
        return Rule(param="", operation="u", value=0, action=rstr)
    
    r_components = rstr.split(":")
    condition = r_components[0]
    #operation = condition_line[1]
    #a = re.split('<|>', condition_line)
    #if "<" in 
    return Rule(param=condition[0], operation=condition[1], value=int(condition[2:]), action=r_components[1])


def workflow_from_line(line: str) -> Workflow:
    s1 = line.split("{")
    name = s1[0]
    rule_strs = s1[1].split("}")[0].split(",")
    rules = [str_to_rule(rstr=s) for s in rule_strs]
    return Workflow(name=name, rules=rules)


#print(first_part_index)
#print(workflow_lines)
#print(part_lines)
    
w = workflow_from_line(workflow_lines[0])
print(w)
