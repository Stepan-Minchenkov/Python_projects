original_line = 'Не знаю, как там в Лондоне, я не была. ' \
               'Может, там собака — друг человека. '\
               'А у нас управдом — друг человека!'

# task 1
number_of_char = len(original_line)
print(f"Шаг1 - Количество символов - {number_of_char}")

# task 2
inverted_line = original_line[::-1]
print(f"Шаг2 - Развернутая строка - {inverted_line}")

# task 3
up_every_word = original_line.title()
print(f"Шаг3 - Все слова с большой буквы - {up_every_word}")

# task 4
upper_case = original_line.upper()
print(f"Шаг4 - Весь текст прописными буквами - {upper_case}")

# task 5
occurences1 = original_line.count('нд')
occurences2 = original_line.count('ам')
occurences3 = original_line.count('о')
print(f"Шаг5 - число вхождений \"нд\": {occurences1}")
print(f"Шаг5 - число вхождений \"ам\": {occurences2}")
print(f"Шаг5 - число вхождений \"о\": {occurences3}")

# task 6
# part of code page 1251
hex_table = {"A": "0xB0", "Б": "0xB1", "В": "0xB2", "Г": "0xB3", "Д": "0xB4",
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
translation = original_line.maketrans(hex_table)
hex_string = original_line.translate(translation)
print(f"Шаг6 - Собственное -- hex вид - {hex_string}")

# task 7 -- covering of original task
(first_sentence,*_) = original_line.split('.')
inverted_sentence = first_sentence.split(' ')
inverted_sentence = inverted_sentence[::-1]
inverted_sentence = ' '.join(inverted_sentence)
print(f"Шаг7 - Развернутое предложение - {inverted_sentence}")

# task 7 -- my own idea of the expectations from the task
inverted_sentence = original_line.replace('!', ' !')
inverted_sentence = inverted_sentence.replace('.', ' .')
inverted_sentence = inverted_sentence.replace(',', ' ,')
inverted_sentence = inverted_sentence.split(' ')
inverted_sentence = inverted_sentence[::-1]
inverted_sentence = ' '.join(inverted_sentence)
inverted_sentence = inverted_sentence.replace('! ', '!')
inverted_sentence = inverted_sentence.replace('. ', '.')
inverted_sentence = inverted_sentence.replace(', ', ',')
print(f"Шаг7 - Развернутое предложение (дополненое) - {inverted_sentence}")

# task 8
print(f"Шаг8 - Исходная строка - {original_line}")