import os.path, sys, io
from jsonFile import jsonFile

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Finder:
    def __init__(self):
        # "cs", "de", "en", "es", "es_al", "it", "pl", "ru"
        # self.locs = ["pl", "en", "cs", "de", "es", "it", "ru"]
        self.locs = ["pl", "en", "ru"]
        # self.settings = "settings.txt"
        self.locs_data = {}
        # self.get_data()

    def get_data(self):
        for loc in self.locs:
            if loc not in self.locs_data:
                self.get_data_from_file(loc)
        # print()
        # відсікає усі локалізації, які не вдалось завантажити
        self.locs = self.locs_data.keys() # list

    def get_data_from_file(self, loc):
        filename = resource_path(os.path.join("locs", loc + ".json"))
        if os.path.isfile(filename):
            self.locs_data[loc] = jsonFile(filename)
            # print(f"Файл '{filename}' успішно завантажено")
        else:
            print(f"Файл '{filename}' не знайдено")

    def print_value(self, loc_name, value):
        if value:
            print(f"{loc_name}: {value}")
        else:
            print(f"{loc_name}: Ключ не знайдено.")

    # основне призначення класу
    def input(self):
        if not self.locs_data: #  is None
            self.get_data()

        print("Введіть q, й або quit для виходу")
        while True:
            # print("Введіть ключ: ", end="")
            key = input("Введіть ключ: ")
            if key == 'q' or  key == "quit" or key == "й":
                break
            
            self.find(key)

    def find(self, key : str):
        key = key.strip()
        
        # print("------------------")
        # print()
        # print(key)
        for loc_name, loc in self.locs_data.items():
            value = loc.get_value(key)
            self.print_value(loc_name, value)
        print()
    
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    finder = Finder()
    finder.get_data()
    # print(finder.locs_data)

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            finder.find(arg) # key
    else:
        finder.input()
