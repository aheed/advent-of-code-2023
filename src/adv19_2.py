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
            #new_filters = new_filters + [top, bottom]
            new_filters = new_filters + [zz for zz in [top, bottom] if get_nof_combinations(filter=zz) > 0]

        filters = new_filters
    assert(len(filters) == 0) # last rule should always be unconditional
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
#a, b, c = divide_filter(filter=generous_filter, rule=workflows["lnx"].rules[0])
#print(get_nof_combinations(a), get_nof_combinations(b), get_nof_combinations(c))

result = nof_combos_by_workflow(filter=generous_filter, workflow=workflows["in"])
print(result)
result_b = sum([get_nof_combinations(filter=f) for f in accepted_filters])
print(result_b)

# 167409079868000 is ex result
# 199630070686152 is too high
# 124332452265904 is too low

def calc_nof_accepted_values(param: str) -> int:
    filter_in_range: list[bool] = [False] * len(accepted_filters) # same index as accepted_filters
    total = 0
    for n in range(1, 4000):
        n_is_accepted = False
        for f_ix in range(len(accepted_filters)):            
            if accepted_filters[f_ix].min[param] == n:
                filter_in_range[f_ix] = True
            if filter_in_range[f_ix]:
                n_is_accepted = True
            if accepted_filters[f_ix].max[param] == n:
                filter_in_range[f_ix] = False
        if n_is_accepted:
            total = total + 1
    return total

#res2 = calc_nof_accepted_values("x") * calc_nof_accepted_values("m") * calc_nof_accepted_values("a") * calc_nof_accepted_values("s")
#print(res2)

def max_vals(param: str) -> list[int]:
    return [f.max[param] for f in accepted_filters]

def min_vals(param: str) -> list[int]:
    return [f.min[param] for f in accepted_filters]

max_v = max_vals("x") + max_vals("m") + max_vals("a") + max_vals("s")
min_v = min_vals("x") + min_vals("m") + min_vals("a") + min_vals("s")
all_vals = list(set(max_v + min_v)) # remove duplicates

#########################
def intersect_param(f1: Filter, f2: Filter, param: str) -> tuple[int, int]:
    intersection_min = max(f1.min[param], f2.min[param])
    intersection_max = min(f1.max[param], f2.max[param])
    return (intersection_min, intersection_max)

def calc_overlapping_combos(f1: Filter, f2: Filter) -> int:
    x_min, x_max = intersect_param(f1=f1, f2=f2,  param="x")
    m_min, m_max = intersect_param(f1=f1, f2=f2,  param="m")
    a_min, a_max = intersect_param(f1=f1, f2=f2,  param="a")
    s_min, s_max = intersect_param(f1=f1, f2=f2,  param="s")
    intersection_filter = Filter(min={"x": x_min, "m": m_min, "a": a_min, "s": s_min}, max={"x": x_max, "m": m_max, "a": a_max, "s": s_max})
    return get_nof_combinations(filter=intersection_filter)

included_filters: list[Filter] = []
total_overlapping = 0
for accepted in accepted_filters:
    for included in included_filters:
        new_overlap = calc_overlapping_combos(f1=included, f2=accepted)
        if new_overlap > 0:
            print("overlap!")
        total_overlapping = total_overlapping + new_overlap
    included_filters.append(accepted)
print("zzz")
print(result_b)
print(total_overlapping)
print(result_b - total_overlapping)
print("zzzz")

t = Filter(min={"x": 1, "m": 1, "a": 1, "s": 1}, max={"x": 1000, "m": 2000-100, "a": 3000, "s": 3001})
t2 = Filter(min={"x": 1000, "m": 2000, "a": 3000, "s": 3000}, max={"x": 4000, "m": 4000, "a": 4000, "s": 4000})
ol = calc_overlapping_combos(f1=t, f2=t2)
print(ol)

#########################

"""
def calc_nof_combos(filters: list[Filter], param: str) -> int:
    total = 0
    for i in range(len(all_vals)):
        limit = all_vals[i]
        if param == "s":
            if any((True if (limit >= f.min[param] and limit <= f.max[param]) else False for f in filters)):
                total = total + 1 #temp!!!!!!!!!!!!
        else:
            remaining_filters = [f for f in filters if (limit >= f.min[param] and limit <= f.max[param])]
            if len(remaining_filters) > 0:
                match param:
                    case "x":
                        next_param = "m"
                    case "m":
                        next_param = "a"
                    case "a":
                        next_param = "s"
                    case _:
                        assert(False)
                total = total + calc_nof_combos(filters=remaining_filters, param=next_param)
        if param == "x":
            print(i)
    return total

res3 = calc_nof_combos(filters=accepted_filters, param="x")
print(res3)
"""

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

Still not good enough! The filters still need to be disjoint.
Perhaps Iterate all combos of max- and min values. Each "hit" (any filter is on) adds to the total size_of_current_range("x") * size_of...

Pruned iteration?
  iterate all numbers 1-4000 or "significant range limits" for "x"
    select all "on" filters
    iterate all numbers 1-4000 or "significant range limits" for "m"
        ...
        etc
  Too slow!!!
"""

