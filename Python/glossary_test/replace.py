def replace_and_print(content, char, new_char):
    # num_replacements = content.count(char)
    print(char, content.count(char))
    return content.replace(char, new_char)
    

def read_and_replace(filename):
    content = None
    # Відкриття файлу у режимі читання
    with open(filename, 'r', encoding='utf-8-sig') as file:
        # Зчитування вмісту файлу
        content = file.read()
        
        content = replace_and_print(content, '«', '"')
        content = replace_and_print(content, '»', '"')
        content = replace_and_print(content, '“', "'")
        content = replace_and_print(content, '”', "'")
        content = replace_and_print(content, '....', "...")
        
        # Повернення в початок файлу для перезапису
        # file.seek(0)
        # Перезапис вмісту файлу
        # file.write(content)
        # Обрізка файлу, якщо новий вміст коротший за попередній
        # file.truncate()
        
    with open(filename, 'w', encoding='utf-8-sig') as file:
        file.write(content)
        
        # return content

# Замінює існуючий файл
def write_file(filename, content):
    # Відкриття файлу у режимі запису
    with open(filename, 'w', encoding='utf-8-sig') as file:
        file.write(content)

def add_write_file(filename):
    # Відкриття файлу у режимі додавання
    with open(filename, 'a', encoding='utf-8-sig') as file:
        file.write("ADDITIONAL_DATA")

filename = 'SQ116_TerryDead.d_RAW.json'
content = read_and_replace(filename)
