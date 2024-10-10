import os
import sys
import io
from TMX_Wrapper import TMX_Wrapper
from json_module.jsonFile import jsonFile

from Glossary import Glossary
from Glossary_sync import Glossary_sync

# створює глосарій на основі переданих tmx і json
class TMX_Glossary(TMX_Wrapper):
    def __init__(self, tmx_file):
        super().__init__(tmx_file)

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
        
def run_create_glossary(glossary_name, json_name):
    tmx_path = os.path.normpath("D:\\Archolos\\Archolos_edit\\DialogeOmegaT\\omegat\\project_save.tmx")
    json_path = os.path.normpath(r"D:\Dropbox\Archolos\CoM_localization_repository\pl\Scripts\Content\Story")
    json_path = os.path.join(json_path, json_name)
    # print(json_path)

    if os.path.isfile(tmx_path) and os.path.isfile(json_path):
        wrapper = TMX_Glossary(tmx_path)
        glossary = wrapper.create_glossary(json_path)
        print(glossary_name, len(glossary.content))
        TMX_Glossary.write_glossaries(glossary, glossary_name) # перезаписує усі глосарії!

def rewrite_glossaries(glossary_name : str):
    path = os.path.join("D:\\Archolos\\Archolos_edit\\DialogeOmegaT\\glossary", glossary_name)
    path = os.path.normpath(path)
    glossary = Glossary(path)

    TMX_Glossary.write_glossaries(glossary, glossary_name)

# Запуск програми
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # run_create_glossary("Items.txt", "Mod_Text.d.json")
    # print()
    # run_create_glossary("names.txt", "Mod_NPC_Names.d.json")
    rewrite_glossaries("names.txt") #   "glossary.txt" "names.txt" "Items.txt"
