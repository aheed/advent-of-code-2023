import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

digits_map = {'one': '1',
 'two': '2',
 'three': '3',
 'four': '4',
 'five': '5',
 'six': '6',
 'seven': '7',
 'eight': '8',
 'nine': '9'}

def number_at_start(sub_line: str) -> str | None:
    if sub_line[0].isnumeric():
        return sub_line[0]
    
    return next((digits_map[key] for key in digits_map.keys() if sub_line.startswith(key)), None)

def get_number(line: str) -> int:
    digits = [n_a_s for i in range(len(line)) if (n_a_s := number_at_start(line[i:]))]
    return int(digits[0] + digits[-1])

print(sum([get_number(line) for line in lines]))
