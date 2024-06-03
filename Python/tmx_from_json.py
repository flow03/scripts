import os
import sys
# import time
import io
import shutil
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from tmx_module.TMX_Merger import TMX_Merger, norm_tu
from json_module.jsonFile import jsonFile
from glossary_test.replace import replace_folder

# ----------------------------------------------------

# def run_repos(repositories_path):
#     if os.path.isdir(repositories_path):
#         merger = TMX_Merger()
#         merger.merge_repos(repositories_path)

def backup(file_path):
    if os.path.isfile(file_path):
        file_path = os.path.abspath(file_path)
        new_path = file_path + ".bak"
        shutil.copy(file_path, new_path) # перезаписує файл, якщо він існує

def run():
    pl_json = jsonFile()
    # replace_folder("pl")
    pl_json.load_loc("pl")

    uk_json = jsonFile()
    # replace_folder("uk")
    uk_json.load_loc("uk")

    filepath = "project_save.tmx"
    backup(filepath)
    tmx_file = TMX_Merger(filepath)
    # tmx_file = TMX_Merger()
    tmx_file.load_json(pl_json, uk_json, "[DEEPL]")
    tmx_file.create(filepath)

def run_tu_test():
    tu = norm_tu.create_tu("Польський текст", "Український текст")
    tu.add_uk_text("[Додатковий текст]") # не використовувати <>
    tu_2 = norm_tu.create_tu("Żądło rzecznego krwiopijcy", "Жало річкового шершня", "Gliban")
    tu_2.add_uk_text("[DEEPL]")

    tmx_file = TMX_Merger()
    tmx_file.tu_dict[tu.get_pl_text()] = tu
    tmx_file.tu_dict[tu_2.get_pl_text()] = tu_2
    tmx_file.create("tu_test.tmx")

# Запуск програми
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    run()
    # run_tu_test()
