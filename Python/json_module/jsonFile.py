import json
import io
import sys
import os
from shutil import move

def import_tmx():
    tmx_dir = os.path.abspath(os.path.join(__file__, '..', '..', 'tmx'))
    # tmx_dir = os.path.join(tmx_dir, 'tmx')
    sys.path.append(tmx_dir)
    # print(tmx_dir)

def tests_path():
    # parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    parent_dir = os.path.abspath(os.path.dirname(__file__))
    # print(parent_dir)

    parent_dir = os.path.dirname(parent_dir)
    # print(parent_dir)
    tmx_dir = os.path.join(parent_dir, 'tmx')
    sys.path.append(tmx_dir)
    # print(tmx_dir)
    # test = os.path.abspath(os.path.join(__file__, '..\..'))
    test = os.path.join(__file__, '..', '..')
    print(test)
    test = os.path.abspath(test)
    print(test)
    print(os.sep)

# import_tmx()
# from TMX_Merger import check_ext

class jsonFile():
    def __init__(self, json_file = None):
        self.data = {}
        # self.repeat = []
        # self.repeat = 0
        # self.files = 0
        
        if json_file:
            self.load_file(json_file) # використовує add
    
    def add(self, json_file):
        with open(json_file, 'r', encoding='utf-8-sig') as file: # відкриття файлу з кодуванням UTF-8-BOM
            try:
                loaded_data = json.load(file) # конвертує бінарні дані в текстовий рядок
                self.data.update(loaded_data)
                # self.add_repeat(loaded_data)
                # self.files += 1
            except json.JSONDecodeError as e:
                print(f"Неможливо прочитати JSON з файлу '{json_file}'")
                # print(f"Cannot read JSON from file '{json_file}'")
                print(f"Line: {e.lineno}, Column: {e.colno}, {e.msg}")
                # print(e.msg)
                print(f"Content: {e.doc.splitlines()[e.lineno - 1]}")
                sys.exit(1)

    def get_value(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return None

    # шукає у вказаній теці і її підтеках усі json-файли, і завантажує їх
    def load_loc(self, loc_path):
        if os.path.exists(loc_path):
            for root, dirs, files in os.walk(loc_path):
                for file in files:
                    # if check_ext(file, 'json'):
                    if file.endswith(".json"):
                        file_path = os.path.join(root, file)
                        self.add(file_path)

    # перевіряє, чи файл існує, чи має він розширення json, і завантажує його
    def load_file(self, file):
        if os.path.isfile(file):
            if file.endswith(".json"):
                self.add(file)

    # записує поточний об'єкт у файл з вказаним ім'ям
    def write(self, filename):
        with open(filename, 'w', encoding='utf-8-sig') as json_file:
            json.dump(self.data, json_file, ensure_ascii=False, indent=4) # indent це відступи, може бути 2

    # шукає у вказаній теці і її підтеках усі json-файли, і шукає в них вказаний ключ
    @staticmethod
    def find_value(loc_path, key):
        for root, dirs, files in os.walk(loc_path):
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    json_file = jsonFile(file_path)
                    value = json_file.get_value(key)
                    if value:
                        return value
        return None

    # створює txt файл зі списоком json файлів у вказаній теці
    @staticmethod
    def create_txt_list(filename, json_folder):
        if os.path.exists(json_folder):
            file_list = []
            for root, dirs, files in os.walk(json_folder):
                for file in files:
                    if file.endswith(".json"):
                        file_list.append(file)
            with open(filename, 'w', encoding='utf-8') as txt_file:
                for name in file_list:
                    txt_file.write(name + '\n')

    # переміщує json файли у теку pl_back
    @staticmethod
    def move_json_files(json_folder, new_folder):
        if os.path.isdir(json_folder):
            count = 0
            if os.path.isfile(new_folder):
                os.remove(new_folder)
                print("Файл", new_folder, "видалено")
            if not os.path.exists(new_folder):
                os.makedirs(new_folder)
                print("Теку", new_folder, "створено")

            for root, dirs, files in os.walk(json_folder):
                for file in files:
                    if file.endswith(".json"):
                        file_path = os.path.join(root, file)
                        # new_path = os.path.join(new_folder, file)
                        # другим аргументом приймає теку, або нове ім'я файлу
                        move(file_path, new_folder) # The destination path must not already exist.
                        count += 1
            print(count, "json файлів переміщено до", new_folder)

    def write_txt(self, filename):
        with open(filename, 'w', encoding='utf-8') as txt_file:
            for line in self.data.values():
                txt_file.write(line + '\n')

    def read_txt(self, filename):
        with open(filename, 'r', encoding='utf-8') as txt_file:
            lines = txt_file.readlines()

        new_data = dict(zip(self.data.keys(), lines))
        self.data.update(new_data)

        # if lines and self.data:
        #     i = 0
        #     for key in self.data:
        #         self.data[key] = lines[i]
        #         i += 1
        #         if i >= len(lines):
        #             print(f"У txt файлі менше рядків({len(lines)}) ніж у поточному json({len(self.data)})")
        #             break

    # повертає новий jsonFile з підмножиною елементів
    # у вказаному діапазоні зі start по end ВКЛЮЧНО
    def create_range(self, start, end):
        start -= 1
        # end -= 1 # не включно
        keys = list(self.data.keys())
        if start >= 0 and start < end and end <= len(keys): # <= враховує останній елемент, < ні
            keys = keys[start : end] # не включає елемент з індексом end
            new_data = {k: self.data[k] for k in keys} # dictionary comprehension

            result = jsonFile()
            result.data = new_data
            return result

    def remove_newlines(self):
        for key, text in self.data.items():
            self.data[key] = text.replace('\n', "")

def run_create_range(filename : str, start : int, end : int):
    if os.path.isfile(filename):
        file = jsonFile(filename)
        print(f"{filename} ({len(file.data)} елементів)")
        new_file = file.create_range(start, end)

        if new_file:
            name, ext = os.path.splitext(filename)
            # new_filename = name + '_' + str(start) + '-' + str(end) + ext
            new_filename = f"{name}_{start}-{end}{ext}"
            new_file.write(new_filename)
            print(new_filename, "успішно створено")
        else:
            print(f"Помилка створення вказаного діапазону {start}-{end}")

def run_with_argv():
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        
        if filename.endswith(".json"):
        # if check_ext(filename, 'json'):
            json_file = jsonFile(filename)
            print(type(json_file.data))
            value = json_file.get_value('NAME_Bloodfly')
            print(value)
        # else:
            # print(f"File {filename} is not json file")
    else:
        print("Using:")
        print("python script.py <json_filename>")

def run_test():
    repo = "D:\\Dropbox\\Archolos\\CoM_localization_repository\\pl"
    json_loc = jsonFile()
    json_loc.load_loc(repo)
    print("data: ", len(json_loc.data))
    # print("repeat: ", json_loc.repeat)
    # print("files: ", json_loc.files)
    # print(type(json_loc.data))
    key = 'NAME_Bloodfly'
    value = json_loc.get_value(key)
    print(key, ':', value)

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # run_with_argv()
    # run_test()
    path = os.path.join("test", "LOG_Entries.d.json")
    run_create_range(path, 1, 10)
    # run_create_range(path, 3450, 3459)
