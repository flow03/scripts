import os, io, sys
from TMX_Wrapper import TMX_Wrapper
from json_module.jsonFile import jsonFile
from tmx_module.tu_dict import base_tu
from shutil import copy

class TMX_FROM_JSON(TMX_Wrapper):
    def __init__(self, tmx_file):
        super().__init__(tmx_file)

    # завантажує дві json ТЕКИ, щоб передати їх у load_json, і створює tmx файл
    def tmx_from_json(self, pl_path, uk_path):
        pl_json = TMX_Wrapper.get_json(pl_path)
        # replace_quotes_folder(uk_path)
        uk_json = TMX_Wrapper.get_json(uk_path)

        self.load_json(pl_json, uk_json, "[DEEPL]")
        # self.create()  # перезаписує існуючий

    # завантажує два json ФАЙЛИ і створює tmx файл
    def tmx_from_json_file(self, pl_file, uk_file):
        pl_json = jsonFile(pl_file)
        uk_json = jsonFile(uk_file)

        self.load_json(pl_json, uk_json, "[DEEPL]")
        # self.create()  # перезаписує існуючий

    # дописує tmx файл на основі двох переданих json файлів
    # також дописує на початок кожного сегмента переданий рядок
    def load_json(self, pl_json : jsonFile, uk_json : jsonFile, add_text=None):
        counter = 0
        for key, pl_text in pl_json.data.items():
            if pl_text not in self.tmx_file._tu_dict:
                if key in uk_json.data:
                    uk_text = uk_json.data[key]
                    tu = base_tu.create_tu(pl_text, uk_text)
                    if add_text:
                        tu.add_uk_text(add_text)
                    self.tmx_file.add_tu(tu)
                    counter += 1

        print(counter, "нових сегментів додано")

    # об'єднує усі json файли у вказаній теці source_folder в один
    # і створює два однакових файли pl_jsonname і uk_jsonname
    @staticmethod
    def create_pl_source_json(source_folder, pl_jsonname, uk_jsonname):
        pl_source = TMX_Wrapper.get_json(source_folder)

        pl_source.write(pl_jsonname)
        print(f"{pl_jsonname} успішно створено ({len(pl_source.data)} елементів)")

        copy(pl_jsonname, uk_jsonname)
        print(uk_jsonname, "успішно скопійовано")

def create_tmx_from_json():
    tmx_path = os.path.join("test", "project_save.tmx")
    source_folder = os.path.join("test", "source")

    pl_file = os.path.join("test", "pl_source.json")
    uk_file = os.path.join("test", "uk_source.json")

    if os.path.isfile(tmx_path):
        wrapper = TMX_FROM_JSON(tmx_path)
        if '-c' in sys.argv:
            wrapper.create_pl_source_json(source_folder, pl_file, uk_file)
        else:
            wrapper.tmx_from_json_file(pl_file, uk_file)
            wrapper.backup()
            wrapper.create()
    else:
        print(f"Файл {tmx_path} відсутній")

# Запуск програми
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    create_tmx_from_json()

    # if '-c' in sys.argv:
    #     create_txt_from_json()
    # else:
    #     create_tmx_from_txt()
