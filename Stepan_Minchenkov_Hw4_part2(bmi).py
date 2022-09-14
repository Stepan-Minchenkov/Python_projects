_BMI_dict = {'tania': [158, 55, "F", 44],
             'andrey': [180, 100, "M", 32],
             'admin': [176, 112, "M", 38]}

options_text = {'A': "Вывести список пользователей",
                'B': "Посмотреть инфо о пользователе",
                'C': "Изменить данные о пользователе",
                'D': "Удалить выбранного пользователя",
                'E': "Добавить пользователя",
                'F': "Выход"}


def _collect_user_input():
    _input_height = 0
    _input_mass = 0
    _input_sex = 'N'
    _input_age = 0
    # try to read user's input, return if not valid one
    try:
        _input_height = int(input("Enter height in centimeters: "))
        _input_mass = int(input("Enter mass in kilograms: "))
        _input_age = int(input("Enter age in years: "))

        if _input_height <= 0 or _input_mass <= 0 or _input_age <= 0:
            print("Incorrect value is typed (zero or negative)")
            return 200

        _input_sex = (input("Enter male(m) or female(f): ")[0:1]).upper()

        if _input_sex not in ["F", "M"]:
            print("Incorrect sex is provided")
            return 200

    except ValueError:
        print("Input data are not integers")
        return 100

    return [_input_height, _input_mass, _input_sex, _input_age]


def list_users():
    print("All existed users are below:")
    for _user in _BMI_dict.keys():
        print(f"{_user:20}")


def login():
    """
    pure function to return logon name of user
    output -- username
    """
    user = input("Enter requested user: ")
    return user


def request_of_user(func):
    def inner(*args, **kwargs):
        _user = login()
        value = func(user=_user, *args, **kwargs)
        return value
    return inner


@request_of_user
def user_detail(**kwargs):
    _user = kwargs.get("user", '')
    if _user not in _BMI_dict:
        print("There is no such user in the list. Nothing to display.")
        return

    _height, _mass, _sex, _age = _BMI_dict.get(_user)
    _bmi = _calculate_bmi(_mass=_mass, _height=_height)
    print(("User name:" + " " * 30)[:21] + "height: " + "mass: " + "sex: " + "age: " + "BMI: ")
    print(f"{_user:20} {_height:7} {_mass:5} {_sex:4} {_age:4} {_bmi:.1f}")
    wiki_bmi(_bmi)


def wiki_bmi(_bmi):
    _min_bmi_wiki = 9
    _max_bmi_wiki = 60

    print("\n line below is based on Wiki BMI:")

    _print_bmi_graph(_bmi, _max_bmi_wiki, _min_bmi_wiki)


def _print_bmi_graph(_bmi, max_bmi, min_bmi):
    _less = ''
    _high = ''
    _progress_bar1 = ''
    _progress_bar2 = '=' * (max_bmi - min_bmi)

    # to avoid problems with too high or too low values
    if int(_bmi) < min_bmi:
        _less = '|< '

    elif int(_bmi) > max_bmi:
        _high = ' >|'

    else:
        _progress_bar1 = '=' * (int(_bmi) - min_bmi - 1) + '|'
        _progress_bar2 = '=' * (max_bmi - int(_bmi))

    print(f"{_less}{min_bmi}{_progress_bar1}"
          f"{_progress_bar2}{max_bmi}{_high}")


@request_of_user
def update_user(**kwargs):
    _user = kwargs.get("user", '')
    if _user not in _BMI_dict:
        print("There is no such user in the list. Try adding user.")
        return

    result = _collect_user_input()
    if isinstance(result, list):
        _new_height, _new_mass, _new_sex, _new_age = result
        _BMI_dict.update({_user: [_new_height, _new_mass, _new_sex, _new_age]})


@request_of_user
def add_user(**kwargs):
    _user = kwargs.get("user", '')
    if _user in _BMI_dict:
        print("There is such user in the list. Can not add another with the same name.")
        return

    result = _collect_user_input()
    if isinstance(result, list):
        _new_height, _new_mass, _new_sex, _new_age = result
        _BMI_dict[_user] = [_new_height, _new_mass, _new_sex, _new_age]


@request_of_user
def delete_user(**kwargs):
    _user = kwargs.get("user", '')
    rc = _BMI_dict.pop(_user, 0)
    if rc:
        print(f"Deletion of user '{_user}' was successful")
    else:
        print("There is no such user in the list. Can not delete.")


def _calculate_bmi(_mass, _height):
    _height = _height / 100  # to have height in meters
    return _mass / (_height * _height)


def time_to_end():
    return "time to end"


options = {'A': list_users,
           'B': user_detail,
           'C': update_user,
           'D': delete_user,
           'E': add_user,
           'F': time_to_end}


def main():
    while 1:
        try:
            print()
            for _ in options_text.keys():
                print(f"\t{_}: {options_text.get(_)}")
            print()
            input_selection = (input("Choose the option: ")).upper()
            result = options.get(input_selection, lambda: print("Incorrect option selected"))()
            if result == "time to end":
                return
        except:
            break


# call of the function:
main()
