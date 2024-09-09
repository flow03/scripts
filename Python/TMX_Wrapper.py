import os
import sys
from datetime import datetime
import io
from shutil import copy
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from tmx_module.TMX_Merger import TMX_Merger
# from tmx_module.tu_dict import base_tu
# from test.replace_quotes import replace_quotes_folder

# ----------------------------------------------------
class TMX_Wrapper:
    def __init__(self, tmx_file):
        self.tmx_file = TMX_Merger(tmx_file)
        self.filepath = os.path.abspath(tmx_file)

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
    @staticmethod
    def remove_newlines_txt(txt_lines : list):
        new_txt = []
        for line in txt_lines:
            new_txt.append(line.replace('\n', ""))
        
        return new_txt
    #-----------------------------------------------------------

def run_replace_newlines():
    archolos_edit = os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\omegat\project_save.tmx')
    wrapper = TMX_Wrapper(archolos_edit)
    wrapper.tmx_file.remove_newlines()
    wrapper.backup()
    wrapper.create()    # перезаписує існуючий

# Запуск програми
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # run_replace_newlines()
    