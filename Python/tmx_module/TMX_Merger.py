import os
import time
from lxml import etree
from datetime import datetime

class base_tu:
    def __init__(self, tu):
        self.tu = tu
    
    def get_date(self):
        tuv_uk = self.tu.find("./tuv[@lang='uk']")
        changedate_value = tuv_uk.attrib.get('changedate')
        date_time = datetime.strptime(changedate_value, "%Y%m%dT%H%M%SZ")
        return date_time    

    def get_pl_text(self):
        pl_text = self.tu.find("./tuv[@lang='pl']/seg").text
        return pl_text

    def get_uk_text(self):
        uk_text = self.tu.find("./tuv[@lang='uk']/seg").text
        return uk_text

    def equal_pl(self, other_tu : 'base_tu'):
        pl_1_text = self.get_pl_text()
        pl_2_text = other_tu.get_pl_text()
        return pl_1_text == pl_2_text

    def equal_uk(self, other_tu : 'base_tu'):
        uk_1_text = self.get_uk_text()
        uk_2_text = other_tu.get_uk_text()
        return uk_1_text == uk_2_text

    def get_key(self):
        pass
    
    def get_uk_seg(self):
        uk_seg = self.tu.find("./tuv[@lang='uk']/seg")
        return uk_seg

    def add_uk_text(self, text):
        seg_uk = self.get_uk_seg()
        seg_uk.text = text + seg_uk.text
        # seg_uk.text = etree.CDATA(text + seg_uk.text)

class norm_tu(base_tu):
    def __init__(self, tu):
        super().__init__(tu)

    def get_key(self):
        return self.get_pl_text()

    @staticmethod    
    def create_tu(pl_text, uk_text, name = "TMX_Merger"):
        current_time = datetime.now().strftime("%Y%m%dT%H%M%SZ")
        # datetime.utcnow() для отримання UTC часу
        
        # Створення кореневого елемента <tu>
        tu = etree.Element("tu")

        # Створення першого дочірнього елемента <tuv> з мовою "pl"
        tuv_pl = etree.SubElement(tu, "tuv", lang="pl")
        seg_pl = etree.SubElement(tuv_pl, "seg")
        seg_pl.text = pl_text

        # Створення другого дочірнього елемента <tuv> з мовою "uk" та додатковими атрибутами
        tuv_uk = etree.SubElement(tu, "tuv", 
                                lang="uk", 
                                changeid=name, 
                                changedate=current_time, 
                                creationid=name, 
                                creationdate=current_time)
        seg_uk = etree.SubElement(tuv_uk, "seg")
        seg_uk.text = uk_text

        return norm_tu(tu)

class prop_tu(base_tu):
    def __init__(self, tu):
        super().__init__(tu)

    def get_prop_id(self):
        file_text = self.tu.find("./prop[@type='file']").text
        id_text =   self.tu.find("./prop[@type='id']").text
        # if file_text and id_text:
        return (file_text, id_text)

    def get_key(self):
        return self.get_prop_id()

    def prop_equal(self, other_tu : 'prop_tu'):
        return self.get_prop_id() == other_tu.get_prop_id()

    @staticmethod
    def check_prop(tu):
        return tu.find("./prop")

class TMX_Merger():
    def __init__(self, tmx_file = None):
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

        if tmx_file:
            self.add_tmx(tmx_file)

    def add_tmx(self, tmx_file):
        print("------")
        self.parse(tmx_file)
        print(f"{tmx_file} додано")
        # print(f"{os.path.basename(tmx_file)} додано")

    def force_add_tmx(self, tmx_file):
        start_time = time.time()
        print("------")
        self.parse(tmx_file, force=True)
        print(f"{tmx_file} примусово додано")
        print_time(start_time, "Час:")

    def create(self, filename : str, _print_stats = True):
        if _print_stats:
            print("------")
            self.print_stats()
        
        self.create_body()
        
        self.write_file(filename) # 'MERGED_repo.tmx'

        # if start_time:
        #     print("------")
        #     print_time(start_time, "Час виконання:")

    def merge_repos(self, repo_root):
        start_time = time.time()
        print("------")
        for repo in os.listdir(repo_root):
            repo_path = os.path.join(repo_root, repo)
            if os.path.isdir(repo_path):
                save_path = os.path.join(repo_path, 'DialogeOmegaT\omegat\project_save.tmx')
                if os.path.isfile(save_path):  
                    # parse_time = time.time()
                    self.parse(save_path)
                    print(os.path.basename(repo_path), "додано")
                    # print_time(parse_time, "Час:")

        print_time(start_time, "Час:")

    def merge_dir(self, directory):
        # start_time = time.time()
        print("------")
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if check_ext(file_path, "tmx"):
                self.parse(file_path)
                print(os.path.basename(file_path), "додано")
                    
        # self.create('MERGED_dir.tmx', start_time)

    def merge_args(self, *tmx_files):
        # start_time = time.time()
        print("------")
        for file in tmx_files:
            if check_ext(file, "tmx"):
                self.parse(file)
                print(os.path.basename(file), "додано")
                    
        # self.create('MERGED_args.tmx', start_time)

    def parse(self, save_path, force=False):
        tree = etree.parse(save_path)
        # ------
        if self.header is None:
            self.header = tree.find('header')
            self.root.insert(0, self.header)
        # ------
        for tu in tree.xpath("//tu"):
            if prop_tu.check_prop(tu) is None:
                tu = norm_tu(tu)
                tu_text_pl = tu.get_pl_text()
                if tu_text_pl not in self.tu_dict:
                    self.tu_dict[tu_text_pl] = tu
                else:
                    self.replace_tu(tu, force) # False as default
            else: # prop
                # print(f"prop '{get_pl_text(tu)}' знайдено")
                tu = prop_tu(tu)
                prop_id = tu.get_prop_id()
                if prop_id not in self.alt_dict:
                    self.alt_dict[prop_id] = tu
                else:
                    self.replace_prop_tu(tu, force) # False as default

    def replace_tu(self, tu : norm_tu, force=False):
        key = tu.get_pl_text()
        ex_tu = self.tu_dict[key]
        if not tu.equal_uk(ex_tu):
            self.diff += 1
            if not force:
                if (tu.get_date() > ex_tu.get_date()):
                    self.tu_dict[key] = tu
                    self.replace += 1
            else:
                self.tu_dict[key] = tu
                self.replace += 1

    def replace_prop_tu(self, tu : prop_tu, force=False):
        id = tu.get_prop_id()
        ex_tu = self.alt_dict[id]
        if not tu.equal_uk(ex_tu):
            self.alt_diff += 1
            if not force:
                if (tu.get_date() > ex_tu.get_date()):
                    self.alt_dict[id] = tu
                    self.alt_replace += 1
            else:
                self.alt_dict[id] = tu
                self.alt_replace += 1

    def create_body(self):
        for key in sorted(self.tu_dict.keys()):
            self.body.append(self.tu_dict[key].tu)
        
        if self.alt_dict:
            for key in sorted(self.alt_dict.keys()):
                self.body.append(self.alt_dict[key].tu)

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
        with open(tmx_file_path, 'w', encoding='utf-8') as file: # 'wb'
            xml_string = etree.tostring(self.root, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode()
            file.write(xml_string)

# Виводить час, який пройшов зі start_time
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
    ...
