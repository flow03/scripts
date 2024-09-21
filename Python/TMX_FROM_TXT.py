import os, io, sys
from TMX_Wrapper import TMX_Wrapper
# from TMX_FROM_JSON import TMX_FROM_JSON
from tmx_module.tu_dict import base_tu
from shutil import copy

# робота з txt-файлами позбавляє додаткового редагування json файлів після перекладу deepl 
class TMX_FROM_TXT(TMX_Wrapper):
    def __init__(self, tmx_file):
        super().__init__(tmx_file)

    # повертає list з рядків переданого txt файлу
    # TODO можливо, варто перенести у батьківський клас TMX_Wrapper
    @staticmethod
    def get_txt(filename : str):
        if os.path.isfile(filename) and filename.endswith(".txt"):
            with open(filename, 'r', encoding='utf-8') as txt_file:
                lines = txt_file.readlines()
            
            lines = TMX_FROM_TXT.remove_newlines_txt(lines)
            return lines

    # видаляє усі символи '\n' з переданого списку
    @staticmethod
    def remove_newlines_txt(txt_lines : list):
        new_txt = []
        for line in txt_lines:
            new_txt.append(line.replace('\n', ""))
        
        return new_txt
      
    # дописує tmx файл на основі двох txt файлів
    def load_txt(self, pl_txt, uk_txt, add_text=None):
        counter = 0
        pl_txt = self.get_txt(pl_txt)
        uk_txt = self.get_txt(uk_txt)
        new_data = list(zip(pl_txt, uk_txt))

        for pl_text, uk_text in new_data:
            if pl_text not in self.tmx_file._tu_dict:
                tu = base_tu.create_tu(pl_text, uk_text)
                if add_text:
                    tu.add_uk_text(add_text)
                self.tmx_file.add_tu(tu)
                counter += 1

        print(counter, "нових сегментів додано")

    # створює два однакових txt файли
    # на основі json файлів у теці і підтеках source_folder
    @staticmethod
    def create_pl_source_txt(source_folder, pl_txtname, uk_txtname):
        pl_source = TMX_Wrapper.get_json(source_folder)

        pl_source.write_txt(pl_txtname)
        print(f"{pl_txtname} успішно створено ({len(pl_source.data)} елементів)")

        copy(pl_txtname, uk_txtname)
        print(uk_txtname, "успішно скопійовано")

#-----------------------------------------------------------

def create_txt_from_json():
    source_folder = os.path.join("test", "source")
    pl_file = os.path.join("test", "pl_source.txt")
    uk_file = os.path.join("test", "uk_source.txt")

    if os.path.isdir(source_folder):
        TMX_FROM_TXT.create_pl_source_txt(source_folder, pl_file, uk_file)

def create_tmx_from_txt():
    tmx_path = os.path.join("test", "project_save.tmx")
    pl_file = os.path.join("test", "pl_source.txt")
    uk_file = os.path.join("test", "uk_source.txt")

    if os.path.isfile(tmx_path):
        wrapper = TMX_FROM_TXT(tmx_path)
        wrapper.load_txt(pl_file, uk_file, "[DEEPL]")
        wrapper.backup()
        wrapper.create()
    else:
        print(f"Файл {tmx_path} відсутній")

# Запуск програми
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    if '-c' in sys.argv:
        create_txt_from_json()
    else:
        create_tmx_from_txt()
