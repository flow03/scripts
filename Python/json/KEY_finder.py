# import json
import os.path
import sys
import io
# from pathlib import Path
from jsonFile import jsonFile

class Finder:
    def __init__(self):
        self.repo = "D:\\Dropbox\\Archolos\\CoM_localization_repository"    # windows
        self.locs = ["pl", "en", "ru"]
        # self.settings = "settings.txt"
        self.locs_data = {}

    def find(self, key):
        # "cs", "de", "en", "es", "es_al", "it", "pl", "ru"
        
        # print("------------------")
        print()
        print(key)
        for loc in self.locs:
            directory_path = check_path_os(os.path.join(self.repo, loc))
            if directory_path:
                value = jsonFile.find_value_new(directory_path, key)
                self.print_value(value, loc)
            else:
                print(f"Локалізацію '{loc}' не знайдено.")        

    def read_settings(self, settings_path):
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
            lines = [line for line in lines if line]
            lines = [line for line in lines if not line.startswith('#')]
            lines = [line.strip() for line in lines]
        
            for key in lines:
                self.find(key)

        else:
            print(f"Файл '{settings_path}' пустий.")

    def get_data(self):
        for loc in self.locs:
            directory_path = check_path_os(os.path.join(self.repo, loc))
            if directory_path:
                json_loc = jsonFile()
                json_loc.load_loc(directory_path)
                self.locs_data[loc] = json_loc

    def print_value(self, value, loc):
        if value:
            print(f"{loc}: {value}")
        else:
            print(f"{loc}: Ключ не знайдено.")

    def input(self):
        # self.get_data()
        print("Введіть q або quit для виходу")
        while True:
            # print("Введіть ключ: ", end="")
            key = input("Введіть ключ: ")
            if key == 'q' or  key == "quit":
                break
            # print()
            # print(key)
            for loc in self.locs_data:
                value = self.locs_data[loc].get_value(key)
                self.print_value(value, loc)
            print()

# def find_file_os(start_dir, filename):
#     # cycles = 0
#     for root, dirs, files in os.walk(start_dir):
#         # cycles += 1
#         if filename in files:
#             file_path = os.path.join(root, filename)
#             # print(f"Циклів {cycles}")
#             # print(f"Файл '{file_path}' знайдено")
#             return file_path
    
#     # print(f"Циклів {cycles}")
#     # print(f"Файл '{filename}' не знайдено.")
#     # sys.exit(1)
#     return None

# def find_file_Path(start_dir, filename):
#     cycles = 0
#     for file in Path(start_dir).rglob('*.json'):
#         # print(file)
#         cycles += 1
#         if file.name == filename:
#             print(f"Циклів Path {cycles}")
#             print(f"Файл '{file}' знайдено")
#             return file
            
#     print(f"Циклів Path {cycles}")
#     print(f"Файл '{filename}' не знайдено.")
#     # sys.exit(1)
#     return None

def check_path_os(path):
    directory_path = os.path.normpath(path)
    if os.path.exists(directory_path):
        # print(f"Шлях '{directory_path}' не знайдено.")
        # sys.exit(1)
        return directory_path
    else:
        # print(f"Шлях '{directory_path}'") 
        return None
    
# def check_path_Path(path):
#     directory_path = Path(path)
#     directory_path = directory_path.resolve()
#     if not directory_path.exists():
#         print(f"Шлях '{directory_path}' не знайдено.")
#         # sys.exit(1)
#         return None
#     else:
#         print(f"Шлях '{directory_path}'") 
#         return directory_path

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    finder = Finder()
    if '-i' in sys.argv:
        finder.get_data()
        finder.input()
    elif len(sys.argv) == 2:
        if sys.argv[1].endswith(".txt"):
            settings = sys.argv[1]
            finder.read_settings(settings)
        else:
            key = sys.argv[1]
            finder.find(key)
    elif len(sys.argv) == 1:
        finder.read_settings("settings.txt")
    else:
        print("Забагато вхідних аргументів. Використання:")
        # print("")
        print("python script.py <key>")
        print("python script.py <settings.txt>")
        print("python script.py -i")
        print("python script.py")
        sys.exit(1)
