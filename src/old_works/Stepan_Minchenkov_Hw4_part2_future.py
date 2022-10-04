import json

options_text = {'A': "Вывести список пользователей",
                'B': "Посмотреть инфо о пользователе",
                'C': "Изменить данные о пользователе",
                'D': "Удалить выбранного пользователя",
                'E': "Добавить пользователя",
                'F': "Выход"}

"""
According to the Internet
Older adults tend to have more body fat than younger adults with the same BMI.
Women tend to have more body fat than men for an equivalent BMI.

A 2016 study backs this up by noting a BMI of 22.5 for men and 21 for women is healthy.

So warnings is better to start for women at BMI - 1.5 comparing with men.
People older than 60 should receive the same treatment but better to use BMI - 2
BMI is used differently for children (aged 2 to 20). It is calculated in the same way as for
adults but then compared to typical values for other children of the same age.
So we will skip the advices for them.

BMI	        Weight standard
Below 18.5	Underweight
18.5–24.9	Normal weight
25.0–29.9	Overweight
30.0 and higher	Obese
"""


class BMI(object):
    def __init__(self):
        self._current_mass = 0
        self._current_height = 1
        self._current_sex = ''
        self._current_age = 0
        self._current_user = ''
        self._bmi = 0
        self._BMI_dict = {}
        self._collect_user_input()
        super().__init__()

    def _bmi_list_pre_existence(func):
        def inner1(self, *args, **kwargs):
            if kwargs.get("call", '') != "direct_call":
                result = self.read_bmi_list_file("BMI.txt")
                if isinstance(result, int) and result > 0:
                    return

                print("There are no data in BMI dictionary yet. Please fill in.")
                _new_user = self.login
                result = func(self, *args, **kwargs)
                if not isinstance(result, list):
                    return

                _new_height, _new_mass, _new_sex, _new_age = result
                self._BMI_dict[_new_user] = \
                    [_new_height, _new_mass, _new_sex, _new_age]
            else:
                kwargs.pop("call")
                return func(self, *args, **kwargs)

        return inner1

    def request_of_user(func):
        def inner(self, *args, **kwargs):
            _user = self.login
            value = func(self, user=_user, *args, **kwargs)
            return value

        return inner

    @_bmi_list_pre_existence
    def _collect_user_input(self):
        _input_mass = 0
        _input_height = 1
        _input_sex = ''
        _input_age = 0
        # try to read user's input, return if not valid one
        try:
            _input_height = int(input("Enter height in centimeters: ")) / 100  # to have height in meters
            _input_mass = int(input("Enter mass in kilograms: "))
            _input_age = int(input("Enter age in years: "))

            if _input_height <= 0 or _input_mass <= 0 or _input_age <= 0:
                print("Incorrect value is typed (zero or negative)")
                return 200

            _input_sex = (input("Enter male(m) or female(f)?: ")[0:1]).upper()

            if _input_sex not in ["F", "M"]:
                print("Incorrect sex is provided")
                return 200

        except ValueError:
            print("Input data are not integers")
            return 100

        return [_input_height, _input_mass, _input_sex, _input_age]

    def list_users(self):
        print("All existed users are below:")
        for _user in self._BMI_dict.keys():
            print(f"{_user:20}")

    @property
    def login(self):
        """
        pure function to return logon name of user
        output -- username
        """
        user = input("Enter user name: ")
        return user

    @request_of_user
    def user_detail(self, **kwargs):
        _user = kwargs.get("user", '')
        if _user not in self._BMI_dict:
            print("There is no such user in the list. Nothing to display.")
            return

        self._current_height, self._current_mass, self._current_sex,\
            self._current_age = self._BMI_dict.get(self._current_user)
        self._bmi = self._calculate_bmi(_mass=self._current_mass, _height=self._current_height)
        print(("User name:" + " " * 30)[:21] + "height: " + "mass: " + "sex: " + "age: " + "BMI: ")
        print(f"{_user:20} {self._current_height:7} {self._current_mass:5} "
              f"{self._current_sex:4} {self._current_age:4} {self._bmi:.1f}")
        self.wiki_bmi()
        self.calc_bmi()
        self.bmi_suggestions()

    @request_of_user
    def update_user(self, **kwargs):
        _user = kwargs.get("user", '')
        if _user not in self._BMI_dict:
            print("There is no such user in the list. Try adding user.")
            return

        result = self._collect_user_input(call="direct_call")
        if isinstance(result, list):
            _new_height, _new_mass, _new_sex, _new_age = result
            self._BMI_dict.update({_user: [_new_height, _new_mass, _new_sex, _new_age]})

    @request_of_user
    def add_user(self, **kwargs):
        _user = kwargs.get("user", '')
        if _user in self._BMI_dict:
            print("There is such user in the list. Can not add another with the same name.")
            return

        result = self._collect_user_input(call="direct_call")
        if isinstance(result, list):
            _new_height, _new_mass, _new_sex, _new_age = result
            self._BMI_dict[_user] = [_new_height, _new_mass, _new_sex, _new_age]

    @request_of_user
    def delete_user(self, **kwargs):
        _user = kwargs.get("user", '')
        rc = self._BMI_dict.pop(_user, 0)
        if rc:
            print(f"Deletion of user '{_user}' was successful")
        else:
            print("There is no such user in the list. Can not delete.")

    @staticmethod
    def _calculate_bmi(_mass, _height):
        return _mass / (_height * _height)

    def _print_bmi_graph(self, max_bmi, min_bmi):
        _less = ''
        _high = ''
        _progress_bar1 = ''
        _progress_bar2 = '=' * (max_bmi - min_bmi)

        # to avoid problems with too high or too low values
        if int(self._bmi) < min_bmi:
            _less = '|< '

        elif int(self._bmi) > max_bmi:
            _high = ' >|'

        else:
            _progress_bar1 = '=' * (int(self._bmi) - min_bmi - 1) + '|'
            _progress_bar2 = '=' * (max_bmi - int(self._bmi))

        print(f"{_less}{min_bmi}{_progress_bar1}"
              f"{_progress_bar2}{max_bmi}{_high}")

    @request_of_user
    def bmi(self, **kwargs):
        self._current_user = kwargs.get("user", '')
        if self._current_user not in self._BMI_dict:
            print("There is no such user in the existed list. "
                  "Please enter all values.")
            result = self._collect_user_input(call="direct_call")
            if not isinstance(result, list):
                return

            self._current_height, self._current_mass, \
                self._current_sex, self._current_age = result
        else:
            self._current_height, self._current_mass, \
                self._current_sex, self._current_age = self._BMI_dict.get(self._current_user)

        self._bmi = self._calculate_bmi(_mass=self._current_mass, _height=self._current_height)

        return self._bmi

    def wiki_bmi(self):
        _min_bmi_wiki = 9
        _max_bmi_wiki = 60

        print("\n line below is based on Wiki BMI:")

        self._print_bmi_graph(_max_bmi_wiki, _min_bmi_wiki)

    def calc_bmi(self):
        _min_bmi_calc = 16
        _max_bmi_calc = 40
        _BMI_range = \
            {"Category": "BMI range - kg/m2",
             "Severe Thinness": "< 16",
             "Moderate Thinness": "16 - 17",
             "Mild Thinness": "17 - 18.5",
             "Normal": "18.5 - 25",
             "Overweight": "25 - 30",
             "Obese Class I": "30 - 35",
             "Obese Class II": "35 - 40",
             "Obese Class III": "> 40"}

        print("\n line below is based on bmi calculator and its limits:")
        for _ in _BMI_range.keys():
            print(f"\t{_:18s}{_BMI_range.get(_)}")
        print()

        self._print_bmi_graph(_max_bmi_calc, _min_bmi_calc)

    def _bmi_suggestions_print_prep(self, suggestion_table):
        bmi_suggestion = "Unsuccessful"
        temp_table = {}
        for _ in suggestion_table.keys():
            if self._current_age >= _:
                temp_table = suggestion_table.get(_)

        for _ in temp_table.keys():
            if self._bmi >= _:
                bmi_suggestion = temp_table.get(_)

        return bmi_suggestion

    def bmi_suggestions(self, **kwargs):
        # this if is added for testing to make it easier to check all combinations
        if kwargs.get('test') == 1:
            self._bmi = kwargs.get('bmi')
            self._current_age = kwargs.get('age')
            self._current_sex = kwargs.get('sex')
            print("=" * 80)
            print(f"Test run. bmi={self._bmi}, age={self._current_age}, sex={self._current_sex}")

        _BMI_advices_male = \
            {0:
                {0: "You should immediately start eating more calories. Severe underweight.",
                 18.5: "Everything is good with you. Just keep you diet style.",
                 25: "You should decrease the number of calories. You are a bit overweight.",
                 30: "You should immediately start eating fewer calories and change your diet. Obese."},

             60:
                 {0: "You should immediately start eating more calories. Your weight is too low.",
                  18.5: "Everything is good with you.",
                  23: "You should eat a bit less. Your weight is a bit high for your age.",
                  28: "You should immediately stop eating so much. " +
                      "There are risks of severe illnesses due to obese."}}

        _BMI_advices_female = \
            {0:
                {0: "You should immediately start eating more. You looks like skeleton.",
                 18.5: "You are fit. Just keep it.",
                 23.5: "You should count your calories. There are slightly more of them than you need.",
                 28.5: "You should stop eating. You are fat."},
             60:
                 {0: "It would be better for your health to eat more. Your weight is too low.",
                  18.5: "You should not change anything in your diet.",
                  23: "You should control how much you are eating. The weight is a bit high for your age.",
                  28: "You will be ill severely due to obese if you do not stop eating."}}

        if self._current_age < 20:
            print("There are no recommendations for people with age from 2 up to 20")
            return

        # Below there is a classical way with using many if.
        # it works but is not interesting
        print(f"\n The way to display via ifs")
        if self._current_sex == 'M':
            if self._current_age < 60:
                if self._bmi < 18.5:
                    print("You should immediately start eating more calories. Severe underweight.")
                elif 18.5 <= self._bmi < 25:
                    print("Everything is good with you. just keep you diet style.")
                elif 25 <= self._bmi < 30:
                    print("You should decrease the number of calories. you are a bit overweight.")
                elif self._bmi >= 30:
                    print("You should immediately start eating fewer calories and change your diet. Obese.")
            if self._current_age >= 60:
                if self._bmi < 18.5:
                    print("You should immediately start eating more calories. Your weight is too low.")
                elif 18.5 <= self._bmi < 23:
                    print("Everything is good with you.")
                elif 23 <= self._bmi < 28:
                    print("You should eat a bit less. Your weight is a bit high for your age.")
                elif self._bmi >= 28:
                    print("You should immediately stop eating so much. " +
                          "There are risks of severe illnesses due to obese.")

        if self._current_sex == 'F':
            if self._current_age < 60:
                if self._bmi < 18.5:
                    print("You should immediately start eating more. You looks like skeleton.")
                elif 18.5 <= self._bmi < 23.5:
                    print("You are fit. Just keep it.")
                elif 23.5 <= self._bmi < 28.5:
                    print("You should count your calories. There are slightly more of them than you need.")
                elif self._bmi >= 28.5:
                    print("You should stop eating. You are fat.")
            if self._current_age >= 60:
                if self._bmi < 18.5:
                    print("It would be better for your health to eat more. Your weight is too low.")
                elif 18.5 <= self._bmi < 23:
                    print("You should not change anything in your diet.")
                elif 23 <= self._bmi < 28:
                    print("You should control how much you are eating. The weight is a bit high for your age.")
                elif self._bmi >= 28:
                    print("You will be ill severely due to obese if you do not stop eating.")

        # This is a new way with dicts:
        print(f"\n The way to display via dicts")
        if self._current_sex == 'M':
            print(self._bmi_suggestions_print_prep(_BMI_advices_male))
        else:
            print(self._bmi_suggestions_print_prep(_BMI_advices_female))

    def read_bmi_list_file(self, file_name):
        try:
            with open(file_name, "r+") as file:
                self._BMI_dict = json.loads(file.read())
                # print(f"{self._BMI_dict}")
        except FileNotFoundError:
            return None
        except json.JSONDecodeError:
            return None
        return len(self._BMI_dict.items())

    def write_bmi_list_file(self, file_name):
        with open(file_name, "w") as file:
            # file.write(json.dumps(self._BMI_dict, indent=4))
            file.write(json.dumps(self._BMI_dict))
        return 0

    def time_to_end(self):
        self.write_bmi_list_file("BMI.txt")
        return "time to end"


bmi_test = BMI()

options = {'A': bmi_test.list_users,
           'B': bmi_test.user_detail,
           'C': bmi_test.update_user,
           'D': bmi_test.delete_user,
           'E': bmi_test.add_user,
           'F': bmi_test.time_to_end}


def main_bmi():
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
if __name__ == '__main__':
    main_bmi()

# print("Ваш индекс массы тела: {:.1f}".format(bmi_test.bmi()))
# bmi_test.wiki_bmi()
# bmi_test.calc_bmi()
# bmi_test.bmi_suggestions()

# Test combinations for checking all possible messages
# bmi_test.bmi_suggestions(test=1, bmi=18, age=19, sex="M")
# bmi_test.bmi_suggestions(test=1, bmi=18, age=19, sex="F")
#
# bmi_test.bmi_suggestions(test=1, bmi=18, age=20, sex="M")
# bmi_test.bmi_suggestions(test=1, bmi=18, age=20, sex="F")
#
# bmi_test.bmi_suggestions(test=1, bmi=18, age=45, sex="M")
# bmi_test.bmi_suggestions(test=1, bmi=18.5, age=45, sex="M")
# bmi_test.bmi_suggestions(test=1, bmi=24, age=45, sex="M")
# bmi_test.bmi_suggestions(test=1, bmi=25, age=45, sex="M")
# bmi_test.bmi_suggestions(test=1, bmi=26, age=45, sex="M")
# bmi_test.bmi_suggestions(test=1, bmi=30, age=45, sex="M")
# bmi_test.bmi_suggestions(test=1, bmi=31, age=45, sex="M")
#
# bmi_test.bmi_suggestions(test=1, bmi=18, age=60, sex="M")
# bmi_test.bmi_suggestions(test=1, bmi=18.5, age=60, sex="M")
# bmi_test.bmi_suggestions(test=1, bmi=22, age=60, sex="M")
# bmi_test.bmi_suggestions(test=1, bmi=23, age=60, sex="M")
# bmi_test.bmi_suggestions(test=1, bmi=26, age=60, sex="M")
# bmi_test.bmi_suggestions(test=1, bmi=28, age=60, sex="M")
# bmi_test.bmi_suggestions(test=1, bmi=29, age=60, sex="M")
#
# bmi_test.bmi_suggestions(test=1, bmi=18, age=45, sex="F")
# bmi_test.bmi_suggestions(test=1, bmi=18.5, age=45, sex="F")
# bmi_test.bmi_suggestions(test=1, bmi=22, age=45, sex="F")
# bmi_test.bmi_suggestions(test=1, bmi=23.5, age=45, sex="F")
# bmi_test.bmi_suggestions(test=1, bmi=26, age=45, sex="F")
# bmi_test.bmi_suggestions(test=1, bmi=28.5, age=45, sex="F")
# bmi_test.bmi_suggestions(test=1, bmi=29, age=45, sex="F")
#
# bmi_test.bmi_suggestions(test=1, bmi=18, age=60, sex="F")
# bmi_test.bmi_suggestions(test=1, bmi=18.5, age=60, sex="F")
# bmi_test.bmi_suggestions(test=1, bmi=22, age=60, sex="F")
# bmi_test.bmi_suggestions(test=1, bmi=23, age=60, sex="F")
# bmi_test.bmi_suggestions(test=1, bmi=26, age=60, sex="F")
# bmi_test.bmi_suggestions(test=1, bmi=28, age=60, sex="F")
# bmi_test.bmi_suggestions(test=1, bmi=29, age=60, sex="F")
del bmi_test
