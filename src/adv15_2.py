import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

steps = lines[0].split(",")
#print(steps[0], steps[-1])

def hash(in_str: str) -> int:
    h = 0
    for c in in_str:
        h = ((h + ord(c)) * 17) % 256
    return h

#hashes = [hash(in_str=step) for step in steps]
#print(sum(hashes))

from dataclasses import dataclass

@dataclass
class Lens:
    label: str
    focal_length: int

def get_slot_with_label(box: list[Lens], label: str) -> int | None:
    return next((i for i in range(len(box)) if box[i].label == label), None)

boxes: list[list[Lens]] = [[] for _ in range(256)]

for step in steps:
    if "-" in step:
        label = step.split("-")[0]
        box_index = hash(in_str=label)
        if (slot_index := get_slot_with_label(box=boxes[box_index], label=label)) is not None:
            boxes[box_index].pop(slot_index)

    if "=" in step:
        step_parts = step.split("=")
        label = step_parts[0]
        box_index = hash(in_str=label)
        focal_length = int(step_parts[1])
        if (slot_index := get_slot_with_label(box=boxes[box_index], label=label)) is not None:
            boxes[box_index][slot_index].focal_length = focal_length
        else:
            boxes[box_index].append(Lens(label=label, focal_length=focal_length))

print(boxes)