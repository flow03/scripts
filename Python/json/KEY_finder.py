import json
import os.path
import sys
import io
from pathlib import Path
from jsonFile import jsonFile

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

def check_path_os(path):
    directory_path = os.path.normpath(path)
    if os.path.exists(directory_path):
        # print(f"Шлях '{directory_path}' не знайдено.")
        # sys.exit(1)
        return directory_path
    else:
        # print(f"Шлях '{directory_path}'") 
        return None
    
def check_path_Path(path):
    directory_path = Path(path)
    directory_path = directory_path.resolve()
    if not directory_path.exists():
        print(f"Шлях '{directory_path}' не знайдено.")
        # sys.exit(1)
        return None
    else:
        print(f"Шлях '{directory_path}'") 
        return directory_path

# Використовує усі три фукнції - get_path_os, find_file_os, find_value_by_key
def localization(key, path, localizations):
    # "cs", "de", "en", "es", "es_al", "it", "pl", "ru"
    # if not localizations:
        # localizations = ["pl", "en", "de", "ru"]    # default
    
    # print("------------------")
    print()
    print(key)
    for loc in localizations:
        directory_path = check_path_os(os.path.join(path, loc))
        if directory_path:
            value = jsonFile.find_value_new(directory_path, key)
            if value:
                print(f"{loc}: {value}")
            else:
                print(f"{loc}: Ключ не знайдено.")
        else:
            print(f"Локалізацію '{loc}' не знайдено.")        

def read_settings(settings_path, default_path, default_locs): # default_path - шлях до репозиторію
    # Читання файлу
    if check_path_os(settings_path):
        with open(settings_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    else:
        print(f"Файл '{settings_path}' не знайдено: read_settings")
        sys.exit(1)
    
    if lines:
        # Прибираємо лишні пробіли, закоментовані, і пусті рядки
        lines = [line.strip() for line in lines]
        lines = [line for line in lines if line]    # видаляємо пусті рядки
        lines = [line for line in lines if not line.startswith('#')]
        lines = [line.strip() for line in lines]
    
        # Перший рядок - шлях до теки
        directory_path = lines[0]
        directory_path = check_path_os(directory_path)
        if not directory_path:
            print(f"Шлях '{lines[0]}' не знайдено.")
            print(f"Буде використано шлях за замовчуванням '{default_path}'\n")
            directory_path = default_path
    
        # Другий рядок - масив рядків, розділених пробілом, або комою з пробілом
        if len(lines) > 1:
            locs_array = lines[1]
            if lines[1]:
                if "," in locs_array:
                    locs_array = locs_array.replace(",", "")
                locs_array = locs_array.split(" ")
            else:
                locs_array = default_locs
                
        # Третій рядок і далі - пари "назва файлу і ключ"
        if len(lines) > 2:
            keys = []
            for line in lines[2:]:
                # line = line.strip()
                # if not line.startswith("#"):
                # filename, key = line.split()
                keys.append(line.strip())
                # print(f"Назва файлу: {filename}, Ключ: {key}")
            # print(keys)  
            for key in keys:
                localization(key, directory_path, locs_array)
                # print()
    else:
        print(f"Файл '{settings_path}' пустий.")

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    default_path = "D:\Dropbox\Archolos\CoM_localization_repository"    # windows
    default_locs = ["pl", "en", "de", "ru"]    # "cs", "de", "en", "es", "es_al", "it", "pl", "ru"
    if len(sys.argv) == 2:
        if sys.argv[1].endswith(".txt"):
            settings = sys.argv[1]
            read_settings(settings, default_path, default_locs)
        else:
            key = sys.argv[1]
            localization(key, default_path, default_locs)
    elif len(sys.argv) == 1:
        read_settings("settings.txt", default_path, default_locs)
    else:
        print("Забагато вхідних аргументів.")
        print("Використання:")
        print("python script.py <key>")
        print("python script.py <settings.txt>")
        print("python script.py")
        sys.exit(1)
