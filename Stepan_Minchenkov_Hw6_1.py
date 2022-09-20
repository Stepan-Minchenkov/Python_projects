import datetime
import time
import os


def coloring(color_number: int, digit_to_display: str, output_lines: list):
    color = '\033[' + str(color_number) + 'm   ' + '\033[0m'
    blank = '   '
    digits = {
        '0': [color + color + color,
              color + blank + color,
              color + blank + color,
              color + blank + color,
              color + color + color],
        '1': [color + color + blank,
              blank + color + blank,
              blank + color + blank,
              blank + color + blank,
              color + color + color],
        '2': [color + color + color,
              blank + blank + color,
              color + color + color,
              color + blank + blank,
              color + color + color],
        '3': [color + color + color,
              blank + blank + color,
              color + color + color,
              blank + blank + color,
              color + color + color],
        '4': [color + blank + color,
              color + blank + color,
              color + color + color,
              blank + blank + color,
              blank + blank + color],
        '5': [color + color + color,
              color + blank + blank,
              color + color + color,
              blank + blank + color,
              color + color + color],
        '6': [color + color + color,
              color + blank + blank,
              color + color + color,
              color + blank + color,
              color + color + color],
        '7': [color + color + color,
              blank + blank + color,
              blank + blank + color,
              blank + blank + color,
              blank + blank + color],
        '8': [color + color + color,
              color + blank + color,
              color + color + color,
              color + blank + color,
              color + color + color],
        '9': [color + color + color,
              color + blank + color,
              color + color + color,
              blank + blank + color,
              color + color + color],
    }

    for _ in range(len(output_lines)):
        output_lines[_] += digits[digit_to_display][_] + '  '


def main():
    cycle_number = 0
    # 101 - red, 102 - green, 103 - yellow, 104 - blue, 105 - magenta, 106 - turquoise
    base_color = [102, 103, 104, 105, 106]

    while 1:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

        print()  # added just to have better output while running in python where os.system('cls') does not work

        date = str(datetime.datetime.now().time())[:8]
        # print(date)
        list_date = date.split(":")
        lines = [' ', ' ', ' ', ' ', ' ']
        cycle_color = base_color[cycle_number]
        current_part = len(list_date)

        for part in list_date:
            current_part -= 1
            for part_number in part:
                coloring(cycle_color, part_number, lines)

            if not current_part:
                break

            for line_number in range(len(lines)):
                if line_number == cycle_number:
                    lines[line_number] += '\033[' + str(cycle_color) + 'm   ' + '\033[0m  '
                else:
                    lines[line_number] += '     '

        for _ in lines:
            print(_)

        time.sleep(1)
        cycle_number += 1

        if cycle_number == len(base_color):
            cycle_number = 0


if __name__ == '__main__':
    main()
