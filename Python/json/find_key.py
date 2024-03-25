import json
import os.path
import sys
import io

def find_value_by_key(json_file, key):
    # Перевірка наявності файлу
    if not os.path.isfile(json_file):
        print(f"Помилка: файл '{json_file}' не знайдено.")
        sys.exit(1)
    
    # Зчитування JSON та пошук значення за ключем
    # with open(json_file, 'rb') as f: # бінарний режим
    with open(json_file, 'r', encoding='utf-8-sig') as f: # відкриття файлу з кодуванням UTF-8-BOM
        try:
            data = json.load(f) # конвертує бінарні дані в текстовий рядок
        except json.JSONDecodeError:
            print(f"Помилка: неможливо прочитати JSON з файлу '{json_file}'.")
            sys.exit(1)
    
    value = data.get(key)
    if value is not None:
        return value
    else:
        print(f"Ключ '{key}' не знайдено у файлі '{json_file}'.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Using: python script.py <json_file_path> <key>")
        sys.exit(1)
    else:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        json_file = sys.argv[1]
        key = sys.argv[2]
        # json_file = 'your_json_file.json'
        # key = 'your_key'
        
        value = find_value_by_key(json_file, key)
        print(f"Значення для ключа '{key}': {value}")
