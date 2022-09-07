"""
According to
https://www.calculator.net/bmi-calculator.html?ctype=metric&cage=25&csex=m&cheightfeet=5&cheightinch=10&cpound=160&cheightmeter=10&ckg=2&printit=0&x=61&y=18
the typical categories are below:

Category	        BMI range - kg/m2
Severe Thinness   	< 16
Moderate Thinness	16 - 17
Mild Thinness	    17 - 18.5
Normal	            18.5 - 25
Overweight      	25 - 30
Obese Class I	    30 - 35
Obese Class II	    35 - 40
Obese Class III  	> 40

According to
https://en.wikipedia.org/wiki/Body_mass_index#/media/File:BMI_chart.png

values can be between 9 and 60
"""


class BMI(object):
    def __init__(self):
        self._input_mass = 0
        self._input_height = 1
        self._bmi = 0
        self._collect_user_input()
        super().__init__()

    def _collect_user_input(self):
        # try to read user's input, return if not valid one
        try:
            self._input_height = int(input("Enter your height in centimeters: ")) / 100  # to have height in meters
            self._input_mass = int(input("Enter your mass in kilograms: "))
            if self._input_height <= 0:
                print("Zero or negative height is typed")
                exit(200)
        except ValueError:
            print("Input data are not integers")
            exit(100)

    def _calculate_bmi(self):
        self._bmi = self._input_mass / (self._input_height * self._input_height)

    def _print_bmi_graph(self, max_bmi, min_bmi):
        self._less = ''
        self._high = ''
        self._progress_bar1 = ''
        self._progress_bar2 = '=' * (max_bmi - min_bmi)

        # to avoid problems with too high or too low values
        if int(self._bmi) < min_bmi:
            self._less = '|< '

        elif int(self._bmi) > max_bmi:
            self._high = ' >|'

        else:
            self._progress_bar1 = '=' * (int(self._bmi) - min_bmi - 1) + '|'
            self._progress_bar2 = '=' * (max_bmi - int(self._bmi))

        print(f"{self._less}{min_bmi}{self._progress_bar1}"
              f"{self._progress_bar2}{max_bmi}{self._high}")

    @property
    def bmi(self):
        self._calculate_bmi()
        return self._bmi

    def wiki_bmi(self):
        self._min_bmi_wiki = 9
        self._max_bmi_wiki = 60

        print("\n line below is based on Wiki BMI:")

        self._print_bmi_graph(self._max_bmi_wiki, self._min_bmi_wiki)

    def calc_bmi(self):
        self._min_bmi_calc = 16
        self._max_bmi_calc = 40
        self._BMI_range = \
            {"Category":	      "BMI range - kg/m2",
             "Severe Thinness":   "< 16",
             "Moderate Thinness": "16 - 17",
             "Mild Thinness":     "17 - 18.5",
             "Normal":	          "18.5 - 25",
             "Overweight":        "25 - 30",
             "Obese Class I":     "30 - 35",
             "Obese Class II":    "35 - 40",
             "Obese Class III":   "> 40"}

        print("\n line below is based on bmi calculator and its limits:")
        for _ in self._BMI_range.keys():
            print(f"\t{_:18s}{self._BMI_range.get(_)}")
        print(" ")

        self._print_bmi_graph(self._max_bmi_calc, self._min_bmi_calc)


bmi_test = BMI()
print("Ваш индекс массы тела: {:.1f}".format(bmi_test.bmi))
bmi_test.wiki_bmi()
bmi_test.calc_bmi()
del bmi_test
