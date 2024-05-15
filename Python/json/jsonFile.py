import json
import sys
import os

def import_tmx():
    tmx_dir = os.path.abspath(os.path.join(__file__, '..', '..', 'tmx'))
    # tmx_dir = os.path.join(tmx_dir, 'tmx')
    sys.path.append(tmx_dir)
    # print(tmx_dir)
    
def tests():
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

import_tmx()
from TMX_Merger import check_ext

class jsonFile():
    def __init__(self, json_file):
        self.data = None
        
        with open(json_file, 'r', encoding='utf-8-sig') as file: # відкриття файлу з кодуванням UTF-8-BOM
            try:
                self.data = json.load(file) # конвертує бінарні дані в текстовий рядок
                # print(type(self.data))
            except json.JSONDecodeError:
                print(f"Неможливо прочитати JSON з файлу '{json_file}'.")
                # sys.exit(1)
                self.data = None
    
    def get_value(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return None
            

if __name__ == "__main__":
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        
        if check_ext(filename, 'json'):
            json_file = jsonFile(filename)
            print(type(json_file.data))
            value = json_file.get_value('NAME_Bloodfly')
            print(value)
        # else:
            # print(f"File {filename} is not json file")
    else:
        print("Using:")
        print("python script.py <json_filename>")
        