import os
import sys
from datetime import datetime
import io
from shutil import copy
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from tmx_module.TMX_Merger import TMX_Merger
# from tmx_module.tu_dict import base_tu
from json_module.jsonFile import jsonFile
# from test.replace_quotes import replace_quotes_folder
from Glossary import Glossary
from Glossary_sync import Glossary_sync

# ----------------------------------------------------
class TMX_Wrapper:
    def __init__(self, tmx_file):
        self.tmx_file = TMX_Merger(tmx_file)
        self.filepath = os.path.abspath(tmx_file)

    # повертає назву підтеки DialogeOmegaT чи ArcholosOmegaT
    @staticmethod
    def get_folder(path : str):
        parts = os.path.normpath(path).split(os.sep)
        if len(parts) >= 3:
            return parts[-3]

    # створює резервну копію поточного tmx файлу
    def backup(self, filepath = None):
        if not filepath:
            filepath = self.filepath

        if os.path.isfile(filepath):
            current_time = datetime.now().strftime("%Y.%m.%d-%H.%M.%S")
            new_path = filepath + '.' + current_time + ".bak"
            copy(filepath, new_path) # перезаписує файл, якщо такий є
            print(os.path.basename(new_path), "створено")

    # ОБЕРЕЖНО! Перезаписує існуючий tmx файл
    # бажано використовувати разом з backup
    def create(self, filepath = None):
        if not filepath:
            filepath = self.filepath
        # self.backup() # TODO потрібно перелопатити усі застосування create
        self.tmx_file.create(filepath, _print_stats=False)
        print(os.path.basename(filepath), "перезаписано")
    #-----------------------------------------------------------
    # REMOVE NEWLINES
    #-----------------------------------------------------------
    def remove_newlines_tmx(self):
        self.tmx_file.remove_newlines()
        self.create()   # перезаписує існуючий

    @staticmethod
    def remove_newlines_txt(txt_lines : list):
        new_txt = []
        for line in txt_lines:
            new_txt.append(line.replace('\n', ""))
        
        return new_txt
    #-----------------------------------------------------------
    # CREATE GLOSSARY
    #-----------------------------------------------------------
    # створює глосарій на основі переданих tmx і json
    def create_glossary(self, json_path):
        json_file = jsonFile(json_path)
        glossary = Glossary()
        for pl_text in json_file.data.values():
            if pl_text in self.tmx_file._tu_dict:
                uk_text = self.tmx_file._tu_dict[pl_text].get_uk_text()
                glossary.add_line(pl_text, uk_text)

        # glossary.write(glossary_path)
        return glossary

    # перезаписує усі глосарії зі вказаним ім'ям
    @staticmethod
    def write_glossaries(glossary : Glossary, filename : str):
        pathes = Glossary_sync.get_pathes()

        for path in pathes:
            filepath = os.path.join(path, filename)
            glossary.write(filepath)
            print(filepath, "створено")
    
#-----------------------------------------------------------

def run_replace_newlines():
    # wrapper = TMX_Wrapper(os.path.join("test","newlines_test.tmx"))
    wrapper = TMX_Wrapper("project_save_a.tmx")
    wrapper.backup()
    wrapper.remove_newlines_tmx()

def run_create_glossary():
    tmx_path = os.path.normpath("D:\\Archolos\\Archolos_edit\\DialogeOmegaT\\omegat\\project_save.tmx")
    # glossary_path = os.path.join("glossary","Items.txt")

    # Items.txt
    filename = "Items.txt"
    json_path = os.path.normpath(r"D:\Archolos\Archolos_work\ArcholosOmegaT\source\Scripts\Content\Story\Mod_Text.d.json")

    # names.txt
    # filename = "names.txt"
    # json_path = os.path.normpath(r"D:\Archolos\Archolos_work\ArcholosOmegaT\source\Scripts\Content\Story\Mod_NPC_Names.d.json")

    wrapper = TMX_Wrapper(tmx_path)
    glossary = wrapper.create_glossary(json_path)
    print(filename, len(glossary.content))
    # glossary.write(glossary_path)
    # print(glossary_path, "створено")
    TMX_Wrapper.write_glossaries(glossary, filename) # перезаписує усі глосарії!

# Запуск програми
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    run_create_glossary()
    # run_replace_newlines()
    