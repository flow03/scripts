import os
import sys
from datetime import datetime
import io
import shutil
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from tmx_module.TMX_Merger import TMX_Merger, norm_tu
from json_module.jsonFile import jsonFile
from replace_quotes import replace_quotes_folder

# ----------------------------------------------------

class TMX_Wrapper:
    def __init__(self, tmx_file):
        self.tmx_file = TMX_Merger(tmx_file)
        self.filepath = os.path.abspath(tmx_file)

    def backup(self):
        if os.path.isfile(self.filepath):
            # self.filepath = os.path.abspath(self.filepath)
            current_time = datetime.now().strftime("%Y.%m.%d-%H.%M")
            new_path = self.filepath + '.' + current_time + ".bak"
            shutil.copy(self.filepath, new_path) # перезаписує файл
            print(os.path.basename(new_path), "створено")

    def load_loc(self, name):
        loc = jsonFile()
        # replace_quotes_folder(name)
        loc.load_loc(name)
        return loc

    # tmx_from_json
    def tmx_from_json(self, pl_path, uk_path):
        pl_json = self.load_loc(pl_path)
        uk_json = self.load_loc(uk_path)

        # self.backup()
        self.load_json(pl_json, uk_json, "[DEEPL]")
        self.tmx_file.create(self.filepath, is_print=False) # "FROM_JSON.tmx"

    def load_json(self, pl_json, uk_json, add_text=None):
        counter = 0
        for key, pl_text in pl_json.data.items():
            if pl_text not in self.tmx_file.tu_dict:
                if key in uk_json.data:
                    uk_text = uk_json.data[key]
                    tu = norm_tu.create_tu(pl_text, uk_text)
                    if add_text:
                        tu.add_uk_text(add_text)
                    self.tmx_file.tu_dict[pl_text] = tu
                    counter += 1

        print(counter, "нових сегментів додано") 
    
    def replace_uk_text(self, tu_dict, text, replace): # static
        count = 0
        for key in tu_dict:
            uk_seg = tu_dict[key].get_uk_seg()
            if text in uk_seg.text:
                uk_seg.text = uk_seg.text.replace(text, replace)
                count += 1
        return count
    
    # replace_newlines
    def replace_newlines(self):
        count = self.replace_uk_text(self.tmx_file.tu_dict, '\n', "")
        print("Замін \\n", count)
        
        if self.tmx_file.alt_dict:
            alt_count = self.replace_uk_text(self.tmx_file.alt_dict, '\n', "")
            print("Альтернативних замін \\n", alt_count)

        self.tmx_file.create(self.filepath, is_print=False)

def run_tu_test():
    tu = norm_tu.create_tu("Польський текст", "Український текст")
    tu.add_uk_text("[Додатковий текст]") # не використовувати <>
    tu_2 = norm_tu.create_tu("Żądło rzecznego krwiopijcy", "Жало річкового шершня", "Gliban")
    tu_2.add_uk_text("[DEEPL]")

    tmx_file = TMX_Merger()
    tmx_file.tu_dict[tu.get_pl_text()] = tu
    tmx_file.tu_dict[tu_2.get_pl_text()] = tu_2
    tmx_file.create("tu_test.tmx")

def run_tmx_from_json():
    wrapper = TMX_Wrapper("project_save.tmx")
    wrapper.backup()
    wrapper.tmx_from_json("pl", "uk")

def run_replace_newlines():
    wrapper = TMX_Wrapper("replaced_save.tmx")
    wrapper.backup()
    wrapper.replace_newlines()

# Запуск програми
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    run_tmx_from_json()
    # run_replace_newlines()
