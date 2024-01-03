import math
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
class Filter:
    min: dict[str, int]
    max: dict[str, int]

def divide_filter(filter: Filter, rule: Rule) -> tuple[Filter, Filter, Filter]:
    if rule.operation == "u":
        return (filter, Filter(min={"x": 1}, max={"x": 0}), Filter(min={"x": 1}, max={"x": 0}))
    
    old_max = filter.max[rule.param]
    old_min = filter.min[rule.param]
    if rule.operation == "<":
        new_max = min(old_max, rule.value-1)
        new_min = old_min
    else:
        new_max = old_max
        new_min = max(old_min, rule.value+1)

    max_dict = {key: new_max if key == rule.param else filter.max[key] for key in filter.max.keys()}
    min_dict = {key: new_min if key == rule.param else filter.min[key] for key in filter.min.keys()}
    applies = Filter(min=min_dict, max=max_dict)

    top_max = old_max
    top_min = new_max+1
    max_dict = {key: top_max if key == rule.param else filter.max[key] for key in filter.max.keys()}
    min_dict = {key: top_min if key == rule.param else filter.min[key] for key in filter.min.keys()}
    top = Filter(min=min_dict, max=max_dict)

    bottom_max = new_min-1
    bottom_min = old_min
    max_dict = {key: bottom_max if key == rule.param else filter.max[key] for key in filter.max.keys()}
    min_dict = {key: bottom_min if key == rule.param else filter.min[key] for key in filter.min.keys()}
    bottom = Filter(min=min_dict, max=max_dict)
    return (applies, top, bottom)

def get_nof_combinations(filter: Filter) -> int:
    return math.prod([max(0, filter.max[key] - filter.min[key] + 1) for key in filter.max.keys()])

accepted_filters: list[Filter] = []

def nof_combos_by_applicable_rule(filter: Filter, rule: Rule) -> int:
    if rule.action == "A":
        if get_nof_combinations(filter=filter) > 0:
            accepted_filters.append(filter)
        else:
            print("useless filter")
        return get_nof_combinations(filter=filter)
    
    if rule.action == "R":
        return 0
    
    return nof_combos_by_workflow(filter=filter, workflow=workflows[rule.action])

def nof_combos_by_workflow(filter: Filter, workflow: Workflow) -> int:
    combos = get_nof_combinations(filter=filter)
    if combos == 0:
        return 0
    
    total = 0
    filters = [filter]
    for rule in workflow.rules:
        new_filters: list[Filter] = []

        for f in filters:
            applicable, top, bottom = divide_filter(filter=f, rule=rule)
            total = total + nof_combos_by_applicable_rule(filter=applicable, rule=rule)
            new_filters = new_filters + [zz for zz in [top, bottom] if get_nof_combinations(filter=zz) > 0]

        filters = new_filters
    assert(len(filters) == 0) # last rule should always be unconditional
    return total

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

first_part_index = lines.index("")
workflow_lines = lines[:first_part_index]

def str_to_rule(rstr: str) -> Rule:
    if not ":" in rstr:
        return Rule(param="", operation="u", value=0, action=rstr)
    
    r_components = rstr.split(":")
    condition = r_components[0]
    return Rule(param=condition[0], operation=condition[1], value=int(condition[2:]), action=r_components[1])


def str_to_workflow(line: str) -> Workflow:
    s1 = line.split("{")
    name = s1[0]
    rule_strs = s1[1].split("}")[0].split(",")
    rules = [str_to_rule(rstr=s) for s in rule_strs]
    return Workflow(name=name, rules=rules)


workflow_list = [str_to_workflow(s) for s in workflow_lines]
workflows: dict[str, Workflow] = {wf.name: wf for wf in workflow_list}

generous_filter = Filter(min={"x": 1, "m": 1, "a": 1, "s": 1}, max={"x": 4000, "m": 4000, "a": 4000, "s": 4000})

result = nof_combos_by_workflow(filter=generous_filter, workflow=workflows["in"])
print(result)
