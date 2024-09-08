import os.path, sys, io
from jsonFile import jsonFile
from KEY_finder import Finder

class FinderLoader(Finder):
    def __init__(self):
        self.repo = "D:\\Dropbox\\Archolos\\CoM_localization_repository"    # windows
        super().__init__()

    def get_data(self):
        for loc in self.locs:
            if loc not in self.locs_data:
                self.get_data_from_repo(loc)
        print()
        # відсікає усі локалізації, які не вдалось завантажити
        self.locs = self.locs_data.keys() # list

    def get_data_from_repo(self, loc):
        directory_path = os.path.join(self.repo, loc)
        if os.path.isdir(directory_path):
            json_loc = jsonFile()
            json_loc.load_loc(directory_path)
            self.locs_data[loc] = json_loc
            print(f"Локалізацію '{loc}' завантажено з репозиторію")
        else:
            print(f"Локалізацію '{loc}' не знайдено")

    # основне призначення класу
    def create_files(self):
        if not self.locs_data:
            self.get_data()

        for loc in self.locs_data:
            filename = os.path.join("locs", loc + ".json")
            self.locs_data[loc].write(filename)
            print(f"Файл '{filename}' успішно створено")
    
    # розширений пошук
    def find(self, key : str):
        key = key.strip()
        
        # print()
        # print(key)
        for loc in self.locs_data.keys():
            value = self.locs_data[loc].get_value(key)
            self.print_value(loc, value)
        else:
            directory_path = os.path.join(self.repo, loc)
            if os.path.isdir(directory_path):
                value = jsonFile.find_value(directory_path, key)
                self.print_value(loc, value)
            else:
                print(f"Локалізацію '{loc}' не знайдено.")
        print()

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    loader = FinderLoader()
    loader.get_data()
    loader.create_files()
