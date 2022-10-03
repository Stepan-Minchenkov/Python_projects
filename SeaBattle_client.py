import os
import time
import socket
import json

your_field = {
   'A': ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
   'B': ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
   'C': ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
   'D': ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
   'E': ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
   'F': ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
   'G': ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
   'H': ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
   'I': ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
   'K': ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
}

enemy_field = {
   'A': ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
   'B': ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
   'C': ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
   'D': ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
   'E': ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
   'F': ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
   'G': ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
   'H': ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
   'I': ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
   'K': ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
}

your_ships_list = {1: 4, 2: 3, 3: 2, 4: 1}
enemy_ships_list = {1: 4, 2: 3, 3: 2, 4: 1}


def print_field(field):
    """
    To print one game field 10x10 based on filled dictionary, where:
    0 = empty field             - print blank
    1 = your ship               - print #
    2 = missed shot             - print *
    3 = enemy's ship            - print blank (can be turned to $ for debugging)
    4 = zone around sunk ship   - print +
    5 = zone around your ship   - print blank (can be turned to ? for debugging)
    6 = hit ship                - print X

    A, B, C.. lists represent columns.
    Printing is done by forming rows from columns (A1+B1+C1+..., A2+B2+C2+..)

    Input: the dict 10x10 with all filled positions
    Output: None
    """
    out_list = []
    for _ in range(22):
        out_list.append('')
    line_number = 0
    out_list[line_number] = "A B C D E F G H I K "
    line_number += 1
    for letter in field:
        curr_line = line_number
        out_list[curr_line] += "--"
        curr_line += 1
        for point in field[letter]:
            if point == "0":                    # 0 = empty field
                out_list[curr_line] += " "
            elif point == "3":                  # 3 = enemy's ship
                # out_list[curr_line] += "$"
                out_list[curr_line] += " "
            elif point == "5":                  # 5 = zone around your ship
                # out_list[curr_line] += "?"
                out_list[curr_line] += " "
            elif point == "1":                  # 1 = your ship
                out_list[curr_line] += "#"
            elif point == "2":                  # 2 = missed shot
                out_list[curr_line] += "*"
            elif point == "4":                  # 4 = zone around sunk ship
                out_list[curr_line] += "+"
            elif point == "6":                  # 6 = hit ship
                out_list[curr_line] += "X"
            out_list[curr_line] += "|"
            curr_line += 1
            out_list[curr_line] += "--"
            curr_line += 1

    for point in range(len(out_list)):
        if point % 2 or point == 0:
            out_list[point] = '   ' + out_list[point]
        elif point != 0:
            out_list[point] = (str(point // 2) + '  ')[:2] + '|' + out_list[point]

    return out_list


def set_ships(field, ships_list, marker='My', **kwargs):
    """
    Function to take coordinates of all your ships.
    Ships should be set one by one with their coordinates in format A1A2A3A4.
    The coordinates are checked to be in valid range A-K, 1-10 and that the number of ships is right
    (1 - 4cells', 2 - 3cells', 3 - 2cells', 4 - 1cells')
    If coordinate's range is set incorrectly -- exception is generated and program stopped.
    Function has hidden parameters 'test', 'test_data' and extra parameter 'marker'.
    If 'test' is passed -- program expects 'test_data' list with all pre-defined ships' positions
    If 'marker' is set to 'Enemy' -- program is setting enemy's ships
        (useful for debugging/developing, as in such case server and other client are not needed)

    Input:  the dict 10x10 to be filled with all positions
            the list of allowed ships' sizes to be set
            the marker ("My" or "Enemy") to set whose fields to fill (Optional)
            'test' keyword = 1, if test data should be accepted (Optional)
            'test_data' list with the ships' coordinates to be set automatically (Optional and only if 'test'=1)
    Output: the list with the coordinates of set ships
            dict 10x10 with all positions (not directly returned but updated as input mutable dict)

    Note: Current version does not check whether ships are set correctly (without missed cells or diagonally)
    """
    if kwargs.get('test') == 1:
        test_mode = 1
    else:
        test_mode = 0

    if marker == 'Enemy':
        mark = "3"
        test_mode = 1
    else:
        mark = "1"

    list_test_elem = 0
    ship_num = 0
    ships = []
    for _ in ships_list:
        ship_num += ships_list.get(_)

    while ship_num:
        if test_mode == 1:
            list_test = kwargs.get('test_data')
            in_position = list_test[list_test_elem]
            list_test_elem += 1
        else:
            in_position = input("Enter positions of the ships: ").upper()
        ship = []
        temp_ship = {}
        odd = 0
        for var in in_position:
            if odd:
                if var not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
                    raise Exception
                ship[-1] += var
            else:
                if var == "0" and ship != [] and ship[-1][1] == '1':
                    ship[-1] += var
                    odd = not odd
                else:
                    if var not in "ABCDEFGHIK":
                        raise Exception
                    ship.append(var)
            odd = not odd

        ship = sorted(ship)
        for cell in ship:
            letter = cell[0]
            number = cell[1:]
            if field[letter][int(number) - 1] == mark or \
               field[letter][int(number) - 1] == "5":
                print("Ship is set incorrectly relatively to others. Repeat input.")
                ship = ''
                break

        if ship == '':
            continue

        curr_ship = ships_list.get(int(len(ship)), "Error")
        if curr_ship == "Error":
            print("The value for ship length is longer than supported. Repeat input.")
            continue
        if curr_ship == 0:
            print("Ships of such length are already set. Repeat input.")
            continue
        ships_list[int(len(ship))] -= 1

        if mark != "3":
            result = borders(ship)
            for cell in result:
                letter = cell[0]
                number = cell[1:]
                field[letter][int(number) - 1] = "5"

        for cell in ship:
            letter = cell[0]
            number = cell[1:]
            field[letter][int(number)-1] = mark
            temp_ship[cell] = 1

        if test_mode != 1:
            print_all()

        ships.append(temp_ship)

        ship_num = 0
        for _ in ships_list:
            ship_num += ships_list.get(_)

    return ships


def print_all():
    """
    print of both your and enemy's 10x10 fields
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    print()
    you = print_field(your_field)
    enemy = print_field(enemy_field)
    for _ in range(len(you)):
        print(you[_] + "          " + enemy[_])


def main():
    # # for debug purposes -- autofill of your ships
    # temp_list = ['A1A2A3A4', 'C1C2C3', 'E1E2E3', 'G1G2', 'K1K2', 'A6A7', 'C6', 'G6', 'K6', 'K10']
    # your_ships = set_ships(your_field, your_ships_list, test=1, test_data=temp_list)
    your_ships = set_ships(your_field, your_ships_list)
    print("Waiting for the start..")

# for debug purposes -- autofill of enemy's ships
#     enemy = ['A1A2A3A4', 'C1C2C3', 'E1E2E3', 'G1G2', 'K1K2', 'A6A7', 'C6', 'G6', 'K6', 'K10']
#     enemy_ships = set_ships(enemy_field, enemy_ships_list, 'Enemy', test=1, test_data=enemy)
#     print_field(enemy_field)
#     print(enemy_ships)

    # with socket.socket() as sock:
    sock = socket.socket()
    sock.connect(('127.0.0.1', 65432))
    sock.send(str.encode(json.dumps(your_ships)))
    enemy_ships = json.loads(sock.recv(1024))
    for ship in enemy_ships:
        for cell in ship.keys():
            letter = cell[0]
            number = cell[1:]
            enemy_field[letter][int(number) - 1] = "3"

    # # for debug purposes -- set the list of  checked ships
    # # temporary data
    # enemy_ships = [{'K10': 1}]
    # your_ships = [{'K10': 1}]

    shoot(your_field, your_ships, enemy_field, enemy_ships, sock)
    print_all()
    if not your_ships:
        print("You loose!!")
        sock.send(str.encode("End. Congratulations! You win the battle!"))
    else:
        print("You win!!")
        sock.send(str.encode("End. Unfortunately, you loose the battle"))
    time.sleep(5)
    sock.close()


def shoot(yours_field, yours_ships, enemys_field, enemys_ships, curr_socket):
    """
    the process of shooting until either your or enemy's list of ships is empty
    """
    while yours_ships != [] and enemys_ships != []:
        time.sleep(2)
        print_all()
        print("Wait your turn...")

        input_data = curr_socket.recv(1024)
        input_data = bytes.decode(input_data)
        if input_data.split('.')[0] == "End":
            break

        if input_data != "Your turn":
            received_shot = input_data
            letter = received_shot[0]
            number = received_shot[1:]

            for hit_ship in yours_ships:
                if hit_ship.get(received_shot):
                    hit_ship[received_shot] = 0
                    if sum(hit_ship.values()) == 0:
                        yours_ships.remove(hit_ship)
                    break

            if yours_field[letter][int(number) - 1] == "0" or \
                    yours_field[letter][int(number) - 1] == "5":
                yours_field[letter][int(number) - 1] = "2"
                print_all()

            if yours_field[letter][int(number) - 1] == "1":
                yours_field[letter][int(number) - 1] = "6"
                curr_socket.send(str.encode("Your turn"))
                continue

        shoot_position = ''
        letter = ''
        number = ''
        while shoot_position == '':
            shoot_position = input("Where to shoot? ").upper()
            letter = shoot_position[0]
            number = shoot_position[1:]

            if number not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
                raise Exception
            if letter not in "ABCDEFGHIK":
                raise Exception

            if enemys_field[letter][int(number) - 1] == "2" or \
                    enemys_field[letter][int(number) - 1] == "4" or \
                    enemys_field[letter][int(number) - 1] == "6":
                print("You have already fired to this point. Please repeat attempt.")
                shoot_position = ''

        curr_socket.send(str.encode(shoot_position))

        if enemys_field[letter][int(number) - 1] == "0":
            enemys_field[letter][int(number) - 1] = "2"
            print("You missed!")
            continue

        if enemys_field[letter][int(number) - 1] == "3":
            enemys_field[letter][int(number) - 1] = "6"
            print("You hit the ship!")

        for hit_ship in enemys_ships:
            if hit_ship.get(shoot_position):
                hit_ship[shoot_position] = 0
                if sum(hit_ship.values()) == 0:
                    enemys_ships.remove(hit_ship)
                    result = borders(hit_ship.keys())
                    for cell in result:
                        letter = cell[0]
                        number = cell[1:]
                        if enemys_field[letter][int(number) - 1] == "0":
                            enemys_field[letter][int(number) - 1] = "4"
                break


def borders(ships):
    """
    Function to find cells around the ship to know
    where the shooting or setting another ship is impossible
    """
    ship = list(ships)
    temp_result = right_border(ship)
    temp_result += left_border(ship)
    temp_result += down_border(temp_result + ship)
    temp_result += up_border(temp_result + ship)
    temp_result = sorted(set(temp_result + ship))
    result = [item for item in temp_result if item not in ship]
    return result


def right_border(ships):
    """
    finding right border
    """
    result = []
    allowed_letters = "ABCDEFGHI"
    replace_letters = "BCDEFGHIK"
    for item in list(ships):
        for ch in range(len(allowed_letters)):
            if allowed_letters[ch] in item:
                result.append(item.replace(allowed_letters[ch], replace_letters[ch]))
    return result


def left_border(ships):
    """
    finding left border
    """
    result = []
    allowed_letters = "BCDEFGHIK"
    replace_letters = "ABCDEFGHI"
    for item in list(ships):
        for ch in range(len(allowed_letters)):
            if allowed_letters[ch] in item:
                result.append(item.replace(allowed_letters[ch], replace_letters[ch]))
    return result


def down_border(ships):
    """
    finding down border
    """
    result = []
    for item in list(ships):
        if int(item[1:]) < 10:
            result.append(item[0] + str(int(item[1:]) + 1))
    return result


def up_border(ships):
    """
    finding up border
    """
    result = []
    for item in list(ships):
        if int(item[1:]) > 1:
            result.append(item[0] + str(int(item[1:]) - 1))
    return result


if __name__ == '__main__':
    main()
