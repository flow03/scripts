import os
import sys
from datetime import datetime
import io
from shutil import copy
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from tmx_module.TMX_Merger import TMX_Merger, norm_tu
from json_module.jsonFile import jsonFile
from replace_quotes import replace_quotes_folder
from Glossary import Glossary

# ----------------------------------------------------

class TMX_Wrapper:
    def __init__(self, tmx_file):
        self.tmx_file = TMX_Merger(tmx_file)
        self.filepath = os.path.abspath(tmx_file)

    # створює резервну копію поточного tmx файлу
    def backup(self):
        if os.path.isfile(self.filepath):
            current_time = datetime.now().strftime("%Y.%m.%d-%H.%M.%S")
            new_path = self.filepath + '.' + current_time + ".bak"
            copy(self.filepath, new_path) # перезаписує файл, якщо такий є
            print(os.path.basename(new_path), "створено")

    # ОБЕРЕЖНО! Перезаписує існуючий tmx файл
    # бажано використовувати разом з backup
    def create(self):
        self.tmx_file.create(self.filepath, _print_stats=False)
    #-----------------------------------------------------------
    # TMX FROM JSON
    #-----------------------------------------------------------
    # створює json файл на основі усіх json файлів у переданій теці і її підтеках
    @staticmethod
    def get_json(path):
        loc = jsonFile()
        loc.load_loc(path)
        return loc

    # завантажує дві json ТЕКИ, щоб передати їх у load_json, і створює tmx файл
    def tmx_from_json(self, pl_path, uk_path):
        pl_json = TMX_Wrapper.get_json(pl_path)
        # replace_quotes_folder(uk_path)
        uk_json = TMX_Wrapper.get_json(uk_path)

        self.load_json(pl_json, uk_json, "[DEEPL]")
        self.create()  # перезаписує існуючий

    # завантажує два json ФАЙЛИ і створює tmx файл
    def tmx_from_json_file(self, pl_file, uk_file):
        pl_json = jsonFile(pl_file)
        uk_json = jsonFile(uk_file)

        self.load_json(pl_json, uk_json, "[DEEPL]")
        self.create()  # перезаписує існуючий

    # дописує tmx файл на основі двох переданих json файлів
    # також дописує на початок кожного сегмента переданий рядок
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
    #-----------------------------------------------------------
    # TMX FROM TXT
    #-----------------------------------------------------------
    # дописує tmx файл на основі двох txt файлів
    def load_txt(self, pl_txt, uk_txt, add_text=None):
        counter = 0
        pl_txt = self.get_txt(pl_txt)
        uk_txt = self.get_txt(uk_txt)
        new_data = list(zip(pl_txt, uk_txt))

        for pl_text, uk_text in new_data:
            if pl_text not in self.tmx_file.tu_dict:
                tu = norm_tu.create_tu(pl_text, uk_text)
                if add_text:
                    tu.add_uk_text(add_text)
                self.tmx_file.tu_dict[pl_text] = tu
                counter += 1

        print(counter, "нових сегментів додано")

    # повертає list з рядків переданого txt файлу
    @staticmethod
    def get_txt(filename : str):
        if os.path.isfile(filename) and filename.endswith(".txt"):
            with open(filename, 'r', encoding='utf-8') as txt_file:
                return txt_file.readlines()
    #-----------------------------------------------------------
    # REPLACE NEWLINES
    #-----------------------------------------------------------
    def replace_uk_text(self, tu_dict, text, replace): # static
        count = 0
        for key in tu_dict:
            uk_seg = tu_dict[key].get_uk_seg()
            if text in uk_seg.text:
                uk_seg.text = uk_seg.text.replace(text, replace)
                count += 1
        return count
    
    def replace_newlines(self):
        count = self.replace_uk_text(self.tmx_file.tu_dict, '\n', "")
        print("Замін \\n", count)
        
        if self.tmx_file.alt_dict:
            alt_count = self.replace_uk_text(self.tmx_file.alt_dict, '\n', "")
            print("Альтернативних замін \\n", alt_count)

        self.create()  # перезаписує існуючий
    #-----------------------------------------------------------
    # CREATE PL SOURCE
    #-----------------------------------------------------------
    # об'єднує усі json файли у вказаній теці source_folder в один
    # і створює два однакових файли pl_jsonname і uk_jsonname
    @staticmethod
    def create_pl_source_json(source_folder, pl_jsonname, uk_jsonname):
        pl_source = TMX_Wrapper.get_json(source_folder)

        # name = "source"
        # pl_jsonname = os.path.join(dest_folder, "pl_" + name + ".json")
        # uk_jsonname = os.path.join(dest_folder, "uk_" + name + ".json")

        pl_source.write(pl_jsonname)
        print(f"{pl_jsonname} успішно створено ({len(pl_source.data)} елементів)")

        copy(pl_jsonname, uk_jsonname)
        print(uk_jsonname, "успішно скопійовано")

        # pl_source.write_txt(uk_jsonname + ".txt")
        # print(f"{uk_jsonname + ".txt"} успішно створено")
    
    # створює два однакових txt файли
    # на основі json файлів у теці і підтеках source_folder
    @staticmethod
    def create_pl_source_txt(source_folder, pl_txtname, uk_txtname):
        pl_source = TMX_Wrapper.get_json(source_folder)

        pl_source.write_txt(pl_txtname)
        print(f"{pl_txtname} успішно створено ({len(pl_source.data)} елементів)")

        copy(pl_txtname, uk_txtname)
        print(uk_txtname, "успішно скопійовано")

    # об'єднує усі json файли у вказаній теці в один
    # переміщуючи при цьому усі файли у нову теку з префіксом _back
    @staticmethod
    def create_pl_source_json_old(pl_folder, uk_folder):
        pl_source = TMX_Wrapper.get_json(pl_folder)

        name = "source"
        textname = os.path.join(pl_folder, "pl_" + name + ".txt")
        jsonname = os.path.join(pl_folder, "pl_" + name + ".json")

        jsonFile.create_txt_list(textname, pl_folder)
        print(textname, "успішно створено")

        jsonFile.move_json_files(pl_folder, pl_folder + "_back")

        pl_source.write(jsonname)
        print(f"{jsonname} успішно створено ({len(pl_source.data)} елементів)")

        uk_jsonname = os.path.join(uk_folder, "uk_" + name + ".json")
        # pl_source.write(uk_jsonname)
        copy(jsonname, uk_jsonname)
        print(uk_jsonname, "успішно скопійовано")
    #-----------------------------------------------------------
    # CREATE GLOSSARY
    #-----------------------------------------------------------
    def create_glossary(self, json_path, glossary_path):
        json_file = jsonFile(json_path)
        glossary = Glossary()
        for pl_text in json_file.data.values():
            if pl_text in self.tmx_file.tu_dict:
                uk_text = self.tmx_file.tu_dict[pl_text].get_uk_text()
                glossary.add_line(pl_text, uk_text)

        glossary.write(glossary_path)
    #-----------------------------------------------------------

def run_tu_test():
    tu = norm_tu.create_tu("Польський текст", "Український текст")
    tu.add_uk_text("[Додатковий текст]") # не використовувати <>
    tu_2 = norm_tu.create_tu("Żądło rzecznego krwiopijcy", "Жало річкового шершня", "Gliban")
    tu_2.add_uk_text("[DEEPL]")

    tmx_file = TMX_Merger()
    tmx_file.tu_dict[tu.get_pl_text()] = tu
    tmx_file.tu_dict[tu_2.get_pl_text()] = tu_2
    tmx_file.create("tu_test.tmx")

def create_tmx_from_json():
    tmx_path = os.path.join("test", "project_save.tmx")
    source_folder = os.path.join("test", "source")

    pl_file = os.path.join("test", "pl_source.json")
    uk_file = os.path.join("test", "uk_source.json")

    if os.path.isfile(tmx_path):
        wrapper = TMX_Wrapper(tmx_path)
        if '-c' in sys.argv:
            wrapper.create_pl_source_json(source_folder, pl_file, uk_file)
        else:
            wrapper.backup()
            wrapper.tmx_from_json_file(pl_file, uk_file)
    else:
        print(f"Файл {tmx_path} відсутній")

#-----------------------------------------------------------
def create_txt_from_json():
    source_folder = os.path.join("test", "source")
    pl_file = os.path.join("test", "pl_source.txt")
    uk_file = os.path.join("test", "uk_source.txt")

    if os.path.isdir(source_folder):
        TMX_Wrapper.create_pl_source_txt(source_folder, pl_file, uk_file)

def create_tmx_from_txt():
    tmx_path = os.path.join("test", "project_save.tmx")
    pl_file = os.path.join("test", "pl_source.txt")
    uk_file = os.path.join("test", "uk_source.txt")

    if os.path.isfile(tmx_path):
        wrapper = TMX_Wrapper(tmx_path)
        wrapper.load_txt(pl_file, uk_file, "[DEEPL]")
        wrapper.backup()
        wrapper.create()    # перезаписує існуючий
    else:
        print(f"Файл {tmx_path} відсутній")
#-----------------------------------------------------------

def run_replace_newlines():
    wrapper = TMX_Wrapper("test\\newlines_test.tmx")
    wrapper.backup()
    wrapper.replace_newlines()

def run_create_glossary():
    # tmx_path = "tmx_from_json_test.tmx"
    tmx_path = "D:\\Archolos_work\\ArcholosOmegaT\\omegat\\project_save.tmx"
    json_path = "glossary_test\\pl_Mod_Text.d.json"
    glossary_path = "glossary_test\\json_glossary.txt"
    wrapper = TMX_Wrapper(tmx_path)
    wrapper.create_glossary(json_path, glossary_path)
    print(glossary_path, "створено")

# Запуск програми
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # run_tmx_from_json()
    # run_create_glossary()
    # run_replace_newlines()
    if '-c' in sys.argv:
        create_txt_from_json()
    else:
        create_tmx_from_txt()
