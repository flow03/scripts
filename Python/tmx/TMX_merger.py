import os
import time
from lxml import etree
from datetime import datetime

class base_tu:
    def __init__(self, tu):
        self.tu = tu
        pass

class tu(base_tu):
    def __init__(self, tu):
        super().__init__(tu)
        pass

class prop_tu(base_tu):
    def __init__(self, tu):
        super().__init__(tu)
        pass

class TMX_Merger():
    def __init__(self):
        self.root = etree.Element('tmx')
        self.header = None
        self.body = etree.SubElement(self.root, 'body')

        self.tu_dict = {}    # Default translations
        self.alt_dict = {}   # Alternative translations

        # self.repeat = 0
        self.diff = 0
        self.replace = 0
        # self.alt_repeat = 0
        self.alt_diff = 0
        self.alt_replace = 0

    def add_tmx(self, tmx_file):
        print("------")
        self.parse(tmx_file)
        print(f"Додатковий {tmx_file} додано")

    def run(self, directory):
        run_time = time.time()
        print("------")
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                # start_time = time.time()
                save_path = os.path.join(item_path, 'DialogeOmegaT\omegat\project_save.tmx')        
                self.parse(save_path)
                print(os.path.basename(item_path), "додано")
                # print_time(start_time, "Час:")
                    
        print("------")
        self.print_stats()
        
        self.create_body()
        
        self.write_file('MERGED.tmx')

        print("------")
        print_time(run_time, "Час виконання:")

    def parse(self, save_path):
        tree = etree.parse(save_path)
        # ------
        if self.header is None:
            self.header = tree.find('header')
            self.root.insert(0, self.header)
        # ------
        for tu in tree.xpath("//tu"):
            if check_prop(tu) is None:
                tu_text_pl = get_pl_text(tu)
                if tu_text_pl not in self.tu_dict:
                    self.tu_dict[tu_text_pl] = tu
                else:
                    self.replace_tu(tu, tu_text_pl)
            else: # prop
                # print(f"prop '{get_pl_text(tu)}' знайдено")
                prop_id = get_prop_id(tu)
                if prop_id not in self.alt_dict:
                    self.alt_dict[prop_id] = tu
                else:
                    self.replace_prop_tu(tu, prop_id)

    def replace_tu(self, tu, key):
        # key = get_pl_text(tu)
        ex_tu = self.tu_dict[key]
        if not equal_uk(tu, ex_tu):
            self.diff += 1
            if (get_date(tu) > get_date(ex_tu)):
                self.tu_dict[key] = tu
                # print(f"{get_date(ex_tu)} замінено на {get_date(tu)}")
                self.replace += 1
            # else:
                # print(f"{get_date(ex_tu)} залишено, натомість {get_date(tu)}")

    def replace_prop_tu(self, tu, id):
        ex_tu = self.alt_dict[id]
        if not equal_uk(tu, ex_tu):
            self.alt_diff += 1
            if (get_date(tu) > get_date(ex_tu)):
                self.alt_dict[id] = tu
                self.alt_replace += 1

    def create_body(self):
        for key in sorted(self.tu_dict.keys()):
            self.body.append(self.tu_dict[key])
        
        if self.alt_dict:
            for key in sorted(self.alt_dict.keys()):
                self.body.append(self.alt_dict[key])

    def print_stats(self):
        if self.alt_dict:
            print(f"Всього:\t {len(self.tu_dict) + len(self.alt_dict)} ({len(self.tu_dict)} + {len(self.alt_dict)})")
        else:
            print("Всього:\t", len(self.tu_dict))
        print("Відмінностей:", self.diff)
        print("Замін:\t", self.replace)
        if self.alt_dict:
            print("Альтернативних відмінностей:", self.alt_diff)
            print("Альтернативних замін:", self.alt_replace)

    def write_file(self, tmx_file_path):
        # tmx_file_path = os.path.join(directory, 'MERGED.tmx')
        # tmx_file_path = 'MERGED.tmx'
        with open(tmx_file_path, 'wb') as f:
            f.write(etree.tostring(self.root, pretty_print=True, xml_declaration=True, encoding='UTF-8'))

def print_time(start_time, text):
    end_time = time.time()
    execution_time = end_time - start_time
    print(text, execution_time)

# Перевіряє розширення
def check_ext(file_path, ext):
    if os.path.isfile(file_path):
        file_name, file_ext = os.path.splitext(file_path)
        file_ext = file_ext.lstrip('.')
        # print("file_ext", file_ext)
        # print("ext", ext)
        return file_ext == ext
    # else:
        # print(f"Файл {file_path} не існує")
        # return False

