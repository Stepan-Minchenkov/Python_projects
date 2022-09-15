import math

x = 0
y = 0

while 1:
    input_line = input("Enter direction of the move -- (R)ight, (L)eft, (U)p, (D)own and number of steps: ")
    if not input_line:
        break
    direction, steps = input_line.split(' ')
    direction = direction[0:1].upper()
    steps = int(steps)
    if direction == 'R':
        x += steps
    if direction == 'L':
        x -= steps
    if direction == 'U':
        y += steps
    if direction == 'D':
        y -= steps
print(f"{math.sqrt(x*x + y*y)}")
