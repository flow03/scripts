import os

def replace_and_print(content, char, new_char):
    # num_replacements = content.count(char)
    # print(char, content.count(char))
    return content.replace(char, new_char)

def replace_quotes(filename):
    content = None
    with open(filename, 'r', encoding='utf-8-sig') as file:
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

def replace_quotes_folder(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            # if check_ext(file, 'json'):
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                replace_quotes(file_path)    

# Замінює існуючий файл
def write_file(filename, content):
    # Відкриття файлу у режимі запису
    with open(filename, 'w', encoding='utf-8-sig') as file:
        file.write(content)

def add_write_file(filename):
    # Відкриття файлу у режимі додавання
    with open(filename, 'a', encoding='utf-8-sig') as file:
        file.write("ADDITIONAL_DATA")

if __name__ == "__main__":
    filename = 'glossary_test\\SQ116_TerryDead.d_RAW.json'
    replace_quotes(filename)
