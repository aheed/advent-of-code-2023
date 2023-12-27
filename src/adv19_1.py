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

@dataclass(frozen=True)
class Part:
    params: dict[str, int]
    #x: int
    #m: int
    #a: int
    #s: int


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


def str_to_workflow(line: str) -> Workflow:
    s1 = line.split("{")
    name = s1[0]
    rule_strs = s1[1].split("}")[0].split(",")
    rules = [str_to_rule(rstr=s) for s in rule_strs]
    return Workflow(name=name, rules=rules)

"""
def str_to_part(input_str: str) -> Part:
    # Removing the curly braces and splitting the string by commas
    parts: list[str] = input_str.strip("{}").split(',')
    # Creating a dictionary to hold the values with type hint
    values: dict[str, int] = {}
    for part in parts:
        # Splitting each part by '=' and assigning to the dictionary
        key, value = part.split('=')
        values[key.strip()] = int(value.strip())  # Stripping spaces and converting to integer

    # Creating and returning a Part instance with extracted values
    return Part(x=values['x'], m=values['m'], a=values['a'], s=values['s'])
"""

def str_to_part(input_str: str) -> Part:
    # Removing the curly braces and splitting the string by commas
    parts = input_str.strip("{}").split(',')
    # Creating a dictionary to hold the values with type hint
    values: dict[str, int] = {}
    for part in parts:
        # Splitting each part by '=' and assigning to the dictionary
        key, value = part.split('=')
        values[key.strip()] = int(value.strip())  # Stripping spaces and converting to integer

    # Creating and returning a Part instance with the params dictionary
    return Part(params=values)

#print(first_part_index)
#print(workflow_lines)
#print(part_lines)
    
#w = str_to_workflow(workflow_lines[0])
#print(w)
#p = str_to_part(input_str=part_lines[0])
#print(p)

workflow_list = [str_to_workflow(s) for s in workflow_lines]
workflows: dict[str, Workflow] = {wf.name: wf for wf in workflow_list}
parts = [str_to_part(s) for s in part_lines]

print("----")

def part_to_rating(part: Part) -> int:
    #return part.x + part.m + part.a + part.s
    return sum(part.params.values())

def rule_applies(rule: Rule, part: Part) -> bool:
    if rule.operation == "u":
        return True
    
    condition_met = part.params[rule.param] < rule.value
    condition_met = condition_met != (rule.operation == ">")
    return condition_met

def part_is_accepted(part: Part) -> bool:
    global workflows
    wf = workflows["in"]
    print("zzzzzzzzzzzzzzzzzzz")
    while True:
        print(wf.name)
        first_applicable_rule = next((rule for rule in wf.rules if rule_applies(rule=rule, part=part)))
        if first_applicable_rule.action == "A":
            return True
        if first_applicable_rule.action == "R":
            return False
        wf = workflows[first_applicable_rule.action]

accepted_parts = [p for p in parts if part_is_accepted(part=p)]
print("---")

print(sum([part_to_rating(part=p) for p in accepted_parts]))