from collections import deque

_line = 'Не знаю, как там в Лондоне, я не была. ' \
               'Может, там собака — друг человека. '\
               'А у нас управдом — друг человека!'


def process_line(option, original_line):
    _print_skeleton = ["Шаг1 - Количество символов",
                       "Шаг2 - Развернутая строка",
                       "Шаг3 - Все слова с большой буквы",
                       "Шаг4 - Весь текст прописными буквами",
                       "Шаг5 - число вхождений",
                       "Шаг6 - Собственное -- hex вид",
                       "Шаг7 - Развернутое предложение",
                       "Шаг8 - Исходная строка"]

    _hex_table = {"A": "0xB0", "Б": "0xB1", "В": "0xB2", "Г": "0xB3", "Д": "0xB4",
                  "Е": "0xB5", "Ж": "0xB6", "З": "0xB7", "И": "0xB8", "Й": "0xB9",
                  "К": "0xBA", "Л": "0xBB", "М": "0xBC", "Н": "0xBD", "О": "0xBE",
                  "П": "0xBF", "Р": "0xC0", "С": "0xC1", "Т": "0xC2", "У": "0xC3",
                  "Ф": "0xC4", "Х": "0xC5", "Ц": "0xC6", "Ч": "0xC7", "Ш": "0xC8",
                  "Щ": "0xC9", "Ъ": "0xCA", "Ы": "0xCB", "Ь": "0xCC", "Э": "0xCD",
                  "Ю": "0xCE", "Я": "0xCF", "а": "0xD0", "б": "0xD1", "в": "0xD2",
                  "г": "0xD3", "д": "0xD4", "е": "0xD5", "ж": "0xD6", "з": "0xD7",
                  "и": "0xD8", "й": "0xD9", "к": "0xDA", "л": "0xDB", "м": "0xDC",
                  "н": "0xDD", "о": "0xDE", "п": "0xDF", "р": "0xE0", "с": "0xE1",
                  "т": "0xE2", "у": "0xE3", "ф": "0xE4", "х": "0xE5", "ц": "0xE6",
                  "ч": "0xE7", "ш": "0xE8", "щ": "0xE9", "ъ": "0xEA", "ы": "0xEB",
                  "ь": "0xEC", "э": "0xED", "ю": "0xEE", "я": "0xEF",
                  ".": "0x2E", ",": "0x2C", "!": "0x21", "?": "0x3F"}

    _resulted_line = ''

    if option == 1:
        _resulted_line = len(original_line)

    if option == 2:
        _resulted_line = original_line[::-1]

    if option == 3:
        _resulted_line = original_line.title()

    if option == 4:
        _resulted_line = original_line.upper()

    if option == 5:
        check_list = ["нд", "ам", "о"]
        _resulted_line = ''
        for _ in check_list:
            _resulted_line += "\n \"" + _ + "\": " + str(original_line.count(_))

    if option == 6:
        _translation = original_line.maketrans(_hex_table)
        _resulted_line = original_line.translate(_translation)

    if option == 7:
        _inverted_sentence = deque()
        _inverted_sentence.extendleft(original_line.split(' '))
        _resulted_line = str(' '.join(_inverted_sentence))

    if option == 8:
        _resulted_line = original_line

    print(f"{_print_skeleton[option - 1]} - {_resulted_line}")


def main():
    input_line = input("Enter text to work with: ")
    if input_line == '':
        input_line = _line

    while 1:
        try:
            input_option = int(input("Choose option from 1 to 8: "))
        except:
            break

        if input_option not in {1, 2, 3, 4, 5, 6, 7, 8}:
            break

        process_line(input_option, input_line)


# call of the function:
main()
