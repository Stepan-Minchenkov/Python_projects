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

input_mass = 0
input_height = 1
min_bmi_calc = 16
max_bmi_calc = 40
min_bmi_wiki = 9
max_bmi_wiki = 60

BMI_range = \
    {"Category":	      "BMI range - kg/m2",
     "Severe Thinness":   "< 16",
     "Moderate Thinness": "16 - 17",
     "Mild Thinness":     "17 - 18.5",
     "Normal":	          "18.5 - 25",
     "Overweight":        "25 - 30",
     "Obese Class I":     "30 - 35",
     "Obese Class II":    "35 - 40",
     "Obese Class III":   "> 40"}

# try to read user's input, return if not valid one
try:
    input_height = int(input("Enter your height in centimeters: ")) / 100  # to have height in meters
    input_mass = int(input("Enter your mass in kilograms: "))
    if input_height <= 0:
        print("Zero or negative height is typed")
        exit(200)
except ValueError:
    print("Input data are not integers")
    exit(100)

bmi = input_mass / (input_height * input_height)
print("Ваш индекс массы тела: {:.1f}".format(bmi))

# first variant of printing progress line:
# is used for wiki BMI
print("\n line below is based on Wiki BMI:")
min_bmi = min_bmi_wiki
max_bmi = max_bmi_wiki

less = ''
high = ''
progress_bar1 = ''
progress_bar2 = '='*(max_bmi-min_bmi)

# to avoid problems with too high or too low values
if int(bmi) < min_bmi:
    less = '|< '

elif int(bmi) > max_bmi:
    high = ' >|'

else:
    progress_bar1 = '='*(int(bmi)-min_bmi-1) + '|'
    progress_bar2 = '='*(max_bmi-int(bmi))

print(f"{less}{min_bmi}{progress_bar1}{progress_bar2}{max_bmi}{high}")

# second variant of printing progress line:
# is used for the Internet bmi calculator limits
print("\n line below is based on bmi calculator and its limits:")
for _ in BMI_range.keys():
    print(f"\t{_:18s}{BMI_range.get(_)}")
print(" ")
min_bmi = min_bmi_calc
max_bmi = max_bmi_calc

less = ''
high = ''
progress_bar = ['=', ] * (max_bmi-min_bmi)

# to avoid problems with too high or too low values
if int(bmi) < min_bmi:
    less = '|< '

elif int(bmi) > max_bmi:
    high = ' >|'

else:
    progress_bar[int(bmi)-min_bmi-1] = '|'

print(f"{less}{min_bmi}{''.join(progress_bar)}{max_bmi}{high}")
