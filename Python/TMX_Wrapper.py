import os
import sys
from datetime import datetime
import io
import shutil
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

    def backup(self):
        if os.path.isfile(self.filepath):
            current_time = datetime.now().strftime("%Y.%m.%d-%H.%M")
            new_path = self.filepath + '.' + current_time + ".bak"
            shutil.copy(self.filepath, new_path) # перезаписує файл, якщо такий є
            print(os.path.basename(new_path), "створено")

    # tmx_from_json
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
        self.tmx_file.create(self.filepath, is_print=False)  # перезаписує існуючий

    # завантажує два json ФАЙЛИ і створює tmx файл
    def tmx_from_json_file(self, pl_file, uk_file):
        pl_json = jsonFile(pl_file)
        uk_json = jsonFile(uk_file)

        self.load_json(pl_json, uk_json, "[DEEPL]")
        self.tmx_file.create(self.filepath, is_print=False)  # перезаписує існуючий

    # створює новий tmx файл на основі двох переданих json файлів
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

    # replace_newlines
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

        self.tmx_file.create(self.filepath, is_print=False) # перезаписує існуючий
    #-----------------------------------------------------------

    # create_pl_source
    #-----------------------------------------------------------
    # об'єднує усі json файли у вказаній теці source_folder в один
    # і створює два однакових файли у теці призначення dest_folder
    # pl_source.json і uk_source.json
    def create_pl_source_new(self, source_folder, pl_jsonname, uk_jsonname):
        pl_source = TMX_Wrapper.get_json(source_folder)

        # name = "source"
        # pl_jsonname = os.path.join(dest_folder, "pl_" + name + ".json")
        # uk_jsonname = os.path.join(dest_folder, "uk_" + name + ".json")

        pl_source.write(pl_jsonname)
        print(f"{pl_jsonname} успішно створено ({len(pl_source.data)} елементів)")

        shutil.copy(pl_jsonname, uk_jsonname)
        print(uk_jsonname, "успішно скопійовано")
    
    # об'єднує усі json файли у вказаній теці в один, і копіює цей файл у теку uk_folder
    # переміщуючи при цьому усі файли у нову теку з префіксом _back
    def create_pl_source(self, pl_folder, uk_folder):
        pl_source = TMX_Wrapper.get_json(pl_folder)

        name = "source"
        textname = os.path.join(pl_folder, "pl_" + name + ".txt")
        jsonname = os.path.join(pl_folder, "pl_" + name + ".json")

        self.create_json_txt(textname, pl_folder)
        print(textname, "успішно створено")

        self.move_json_files(pl_folder, pl_folder + "_back")

        pl_source.write(jsonname)
        print(f"{jsonname} успішно створено ({len(pl_source.data)} елементів)")

        uk_jsonname = os.path.join(uk_folder, "uk_" + name + ".json")
        # pl_source.write(uk_jsonname)
        shutil.copy(jsonname, uk_jsonname)
        print(uk_jsonname, "успішно скопійовано")

    # створює txt файл зі списоком json файлів у вказаній теці
    def create_json_txt(self, filename, json_folder):
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
    def move_json_files(self, json_folder, new_folder):
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
                        shutil.move(file_path, new_folder) # The destination path must not already exist.
                        count += 1
            print(count, "json файлів переміщено до", new_folder)
    #-----------------------------------------------------------

    # create_glossary
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

def run_tmx_from_json_new():
    tmx_path = os.path.join("test", "project_save.tmx")
    source_folder = os.path.join("test", "source")

    pl_file = os.path.join("test", "pl_source.json")
    uk_file = os.path.join("test", "uk_source.json")

    if os.path.isfile(tmx_path):
        wrapper = TMX_Wrapper(tmx_path)
        if '-c' in sys.argv:
            wrapper.create_pl_source_new(source_folder, pl_file, uk_file)
        else:
            wrapper.backup()
            wrapper.tmx_from_json_file(pl_file, uk_file)
    else:
        print(f"Файл {tmx_path} відсутній")


def run_tmx_from_json():
    tmx_path = os.path.join("test", "tmx_from_json_test.tmx")
    # tmx_path = "D:\\Archolos_work\\ArcholosOmegaT\\omegat\\project_save.tmx"
    pl_folder = os.path.join("test", "pl")
    uk_folder = os.path.join("test", "uk")
    wrapper = TMX_Wrapper(tmx_path)

    if '-c' in sys.argv:
        wrapper.create_pl_source(pl_folder, uk_folder)
    else:
        wrapper.backup()
        wrapper.tmx_from_json(pl_folder, uk_folder)

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
    run_tmx_from_json_new()
    # run_create_glossary()
    # run_replace_newlines()
