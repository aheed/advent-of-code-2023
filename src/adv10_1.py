import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

y_s = 0
while True:
    if "S" in lines[y_s]:
        x_s = lines[y_s].index("S")
        break
    y_s = y_s + 1

print(x_s,y_s)
print(lines[y_s][x_s])

found = False
x = x_s
y = y_s
direction = "e"
orientation = 0
c = lines[y_s][x_s]

east = lines[y_s][x_s+1]
if east == "-":
    x = x_s+1
    y = y_s
    found = True

if east == "J":
    x = x_s+1
    y = y_s-1
    direction = "n"
    orientation = orientation - 90
    found = True

if east == "7":
    x = x_s+1
    y = y_s+1
    direction = "s"
    orientation = orientation + 90
    found = True

# todo: handle the case you can't start going east
assert(found)

cnt = 2
while not (x == x_s and y == y_s):
    c = lines[y][x]

    print(cnt, x, y, c, direction, orientation)

    if direction == "e":
        if c == "-":
            x = x + 1
        elif c == "J":
            y = y - 1
            direction = "n"
            orientation = orientation - 90
        elif c == "7":
            y = y + 1
            direction = "s"
            orientation = orientation + 90
    elif direction == "w":
        if c == "-":
            x = x - 1
        elif c == "L":
            y = y - 1
            direction = "n"
            orientation = orientation + 90
        elif c == "F":
            y = y + 1
            direction = "s"
            orientation = orientation - 90
    elif direction == "n":
        if c == "|":
            y = y - 1
        elif c == "7":
            x = x - 1
            direction = "w"
            orientation = orientation - 90
        elif c == "F":
            x = x + 1
            direction = "e"
            orientation = orientation + 90
    elif direction == "s":
        if c == "|":
            y = y + 1
        elif c == "J":
            x = x - 1
            direction = "w"
            orientation = orientation + 90
        elif c == "L":
            x = x + 1
            direction = "e"
            orientation = orientation - 90

   
    cnt = cnt + 1

print("---")
print(cnt, x, y, c, direction, orientation)
print(cnt)
print(cnt // 2)