import json
import sys
import os

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
            self.add(json_file)
    
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

    # def add_repeat(self, new_data : dict):
    #     for key, value in new_data.items():
    #         if key in self.data:
    #             # self.repeat.append((key, value))
    #             self.repeat += 1
    #         else:
    #             self.data[key] = value

    def get_value(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return None

    def load_loc(self, loc_path):
        if os.path.exists(loc_path):
            for root, dirs, files in os.walk(loc_path):
                for file in files:
                    # if check_ext(file, 'json'):
                    if file.endswith(".json"):
                        file_path = os.path.join(root, file)
                        self.add(file_path)

    def load_file(self, file):
        if os.path.isfile(file):
            if file.endswith(".json"):
                self.add(file)

    def write(self, filename):
        with open(filename, 'w', encoding='utf-8-sig') as json_file:
            json.dump(self.data, json_file, ensure_ascii=False, indent=4) # indent це відступи

    @staticmethod
    def find_value(loc_path, key):
        for root, dirs, files in os.walk(loc_path):
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8-sig') as json_file:
                        try:
                            loaded_data = json.load(json_file)
                            if key in loaded_data:
                                return loaded_data[key]
                        except json.JSONDecodeError:
                            print(f"Cannot read JSON from file '{json_file}'")
        return None

    @staticmethod
    def find_value_new(loc_path, key):
        for root, dirs, files in os.walk(loc_path):
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    json_file = jsonFile(file_path)
                    value = json_file.get_value(key)
                    if value:
                        return value
        return None

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
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # run_with_argv()
    run_test()
