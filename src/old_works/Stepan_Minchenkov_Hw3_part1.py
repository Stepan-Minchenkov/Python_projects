def main():
    preset_value1 = 50
    preset_value2 = 5
    preset_value3 = 7
    # try to read user's input, return if not valid one
    try:
        input_number1 = int(input("Enter number1: "))
        input_number2 = int(input("Enter number2: "))
        input_number3 = int(input("Enter number3: "))

    except ValueError:
        print("Input data are not integers")
        exit(100)

    zero_check = (input_number1 and input_number2 and input_number3 and "Нет нулевых значений!!!") or \
                 (input_number1 or input_number2 or input_number3 or "Введены все нули!")
    print(f"first non-zero input value or warning: {zero_check}")

    if input_number1 > (input_number2 + input_number3):
        print(f"a-b-c = {input_number1 - input_number2 - input_number3}")
    elif input_number1 < (input_number2 + input_number3):
        print(f"b+c-a = {input_number2 + input_number3 - input_number1}")

    if input_number1 > preset_value1 and (input_number2 > input_number1 or input_number3 >input_number1):
        print("Вася")

    if input_number1 > preset_value2 or (input_number2 == preset_value3 and input_number3 == preset_value3):
        print("Петя")

# call of the function:
main()
