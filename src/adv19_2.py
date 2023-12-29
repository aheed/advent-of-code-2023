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

####
    


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

def nof_combos_by_applicable_rule(filter: Filter, rule: Rule) -> int:
    if rule.action == "A":
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
            new_filters = new_filters + [top, bottom]

        filters = new_filters

    return total

###
    
with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

first_part_index = lines.index("")
workflow_lines = lines[:first_part_index]

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


workflow_list = [str_to_workflow(s) for s in workflow_lines]
workflows: dict[str, Workflow] = {wf.name: wf for wf in workflow_list}

######
generous_filter = Filter(min={"x": 1, "m": 1, "a": 1, "s": 1}, max={"x": 4000, "m": 4000, "a": 4000, "s": 4000})
a, b, c = divide_filter(filter=generous_filter, rule=workflows["lnx"].rules[0])
print(get_nof_combinations(a), get_nof_combinations(b), get_nof_combinations(c))

result = nof_combos_by_workflow(filter=generous_filter, workflow=workflows["in"])
print(result)

# 167409079868000 is ex result
# 199630070686152 is too high

@dataclass(frozen=True)
class LimitRange:
    max: int
    min: int

def diff(original: Filter, extra: Filter) -> list[Filter]:
    """
    Returns the union of original and extra as a disjoint set of filters
    """
    ranges: list[dict[str, LimitRange]] = [{}, {}]
    for key in original.max.keys(): #could just as well be extra or min. Keys should be the same.
        top_max = extra.max[key]
        top_min = original.max[key]+1
        ranges[0][key] = LimitRange(max=top_max, min=top_min)
        bottom_max = original.min[key]-1
        bottom_min = extra.min[key]
        ranges[1][key] = LimitRange(max=bottom_max, min=bottom_min)
    
    ret: list[Filter] = []
    for x_ix in range(2): # 0=top, 1=bottom
        for m_ix in range(2):
            for a_ix in range(2):
                for s_ix in range(2):
                    #create filter for combination of conditions and add to result list
                    ret.append(Filter(min={"x": ranges[x_ix]["x"].min, "m": ranges[m_ix]["m"].min, "a": ranges[a_ix]["a"].min, "s": ranges[s_ix]["s"].min}, max={"x": ranges[x_ix]["x"].max, "m": ranges[m_ix]["m"].max, "a": ranges[a_ix]["a"].max, "s": ranges[s_ix]["s"].max}))

    # filter out filters with 0 combinations. Not strictly necessary.
    ret = [f for f in ret if get_nof_combinations(filter=f) > 0]

    # return what is left. Could be empty list.
    return ret
    
"""
Likely cause of incorrect result: reported accepted filters are not disjoint.
To do: 
    collect reported accepted filters
    Reduce the accepted collection to a set of disjoint filters
        Start disjoint collection as a single zero filter.
            For each accepted filter
                For each disjoint filter
                    Create a collection of new disjoint filters that is the "excess" not already covered by the disjoint filter.
                    Add them to the disjoint filter collection.
    sum up combinations of all disjoint filters

Not good enough! Pair-wise comparison of filters as described above will not be enough.
Perhaps a new filter definition with support for arbitrary (disjoint) ranges is what we need.
  How to diff that kind of filter?
  Operations that must be supported:
    divide by rule
    diff (?), maybe not needed. We just need to calc total number of combinations from a collection of filters. OK to iterate 4000 values.    

  List of int
    even indexes are min, odd indexes are max

Maybe just calc total by iterating all 4000 values (x4) will work. Even with old filter definition. No diff needed.
"""