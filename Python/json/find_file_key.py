import json
import os.path
import sys
import io
from pathlib import Path

# os
def find_file_os(start_dir, filename):
    # cycles = 0
    for root, dirs, files in os.walk(start_dir):
        # cycles += 1
        if filename in files:
            file_path = os.path.join(root, filename)
            # print(f"Циклів {cycles}")
            # print(f"Файл '{file_path}' знайдено")
            return file_path
    
    # print(f"Циклів {cycles}")
    # print(f"Файл '{filename}' не знайдено.")
    # sys.exit(1)
    return None

# Path    
def find_file_Path(start_dir, filename):
    cycles = 0
    for file in Path(start_dir).rglob('*.json'):
        # print(file)
        cycles += 1
        if file.name == filename:
            print(f"Циклів Path {cycles}")
            print(f"Файл '{file}' знайдено")
            return file
            
    print(f"Циклів Path {cycles}")
    print(f"Файл '{filename}' не знайдено.")
    sys.exit(1)
    # return None

def find_value_by_key(json_file, key):
    # Перевірка наявності файлу
    # if not json_file.exists():
        # print(f"Файл '{json_file}' не знайдено.")
        # sys.exit(1)
    
    # Зчитування JSON та пошук значення за ключем
    # with open(json_file, 'rb') as f: # відкриття файлу у бінарному режимі
    with open(json_file, 'r', encoding='utf-8-sig') as f: # відкриття файлу з кодуванням UTF-8-BOM
        try:
            data = json.load(f) # конвертує бінарні дані в текстовий рядок
        except json.JSONDecodeError:
            print(f"Неможливо прочитати JSON з файлу '{json_file}'.")
            # sys.exit(1)
            return None
    
    value = data.get(key)
    if value is not None:
        # print(f"Значення для ключа '{key}': {value}")
        return value
    else:
        # print(f"Ключ '{key}' не знайдено у файлі '{json_file}'.")
        # print(f"Ключ '{key}' не знайдено у вказаному файлі.")
        # sys.exit(1)
        return None

def get_path_os(path):
    directory_path = os.path.normpath(path)
    if not os.path.exists(directory_path):
        print(f"Шлях '{directory_path}' не знайдено.")
        # sys.exit(1)
        return None
    else:
        # print(f"Шлях '{directory_path}'") 
        return directory_path
    
def get_path_Path(path):
    directory_path = Path(path)
    directory_path = directory_path.resolve()
    if not directory_path.exists():
        print(f"Шлях '{directory_path}' не знайдено.")
        sys.exit(1)
    else:
        print(f"Шлях '{directory_path}'") 
        return directory_path

# Використовує усі три фукнції - get_path_os, find_file_os, find_value_by_key
def localization(path):
    # "cs", "de", "en", "es", "es_al", "it", "pl", "ru"
    localizations = ["pl", "en", "de", "ru"]
    
    filename = sys.argv[1]
    key = sys.argv[2]
        
    for loc in localizations:
        current_path = os.path.join(path, loc)
        directory_path = get_path_os(current_path)
        if directory_path:
            file_path = find_file_os(directory_path, filename)
            if file_path:
                value = find_value_by_key(file_path, key)
                if value:
                    print(f"{loc}: '{key}': {value}")
                else:
                    print(f"{loc}: Ключ '{key}' не знайдено у файлі '{filename}'.")
            else:
                print(f"{loc}: Файл '{filename}' не знайдено.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Using: python script.py <filename> <key>")
        sys.exit(1)
    else:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        
        # unix_path = "/d/Dropbox/Archolos/CoM_localization_repository/pl"
        windows_path = "D:\Dropbox\Archolos\CoM_localization_repository"
        # directory_path = get_path_os(windows_path)
        
        localization(windows_path)
                    
        # file_path = find_file_os(directory_path, filename)
        # file_path = find_file_Path(directory_path, filename)
        # value = find_value_by_key(file_path, key)

#python find_file_key.py Mod_Text.d.json NAME_Bloodfly
