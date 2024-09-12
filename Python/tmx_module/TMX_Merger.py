import os
import time
from lxml import etree
from tmx_module.tu_dict import base_tu, prop_tu, tu_dict

class TMX_Merger():
    def __init__(self, tmx_file = None):
        self.root = etree.Element('tmx')
        self.header = None
        self.body = etree.SubElement(self.root, 'body')

        self._tu_dict = tu_dict()    # Default translations
        self._alt_dict = tu_dict()   # Alternative translations

        # self.repeat = 0
        # self.diff = 0
        # self.replace = 0
        # self.alt_repeat = 0
        # self.alt_diff = 0
        # self.alt_replace = 0

        if tmx_file:
            self.add_tmx(tmx_file)

    def add_tmx(self, tmx_file):
        if os.path.isfile(tmx_file):
            # print("------")
            self.parse(tmx_file)
            print(f"{tmx_file} додано")
            # print(f"{os.path.basename(tmx_file)} додано")
        else:
            print(f"Файл {tmx_file} відсутній")

    def force_add_tmx(self, tmx_file):
        start_time = time.time()
        print("------")
        self.parse(tmx_file, force=True)
        print(f"{tmx_file} примусово додано")
        print_time(start_time, "Час:")

    def add_tu(self, tu):
        if prop_tu.check_prop(tu) is None:
            self._tu_dict.add(base_tu(tu))
        else: # prop
            self._alt_dict.add(prop_tu(tu))

    # def add_tu_weak(self, tu):
    #     key = tu.get_key()
    #     if key not in self._tu_dict and key not in self._alt_dict:
    #         self.add_tu(tu)

    def add_tu_force(self, tu):
        if prop_tu.check_prop(tu) is None:
            self._tu_dict.add(base_tu(tu), force=True)
        else:
            self._alt_dict.add(prop_tu(tu), force=True)

    def create(self, filename : str, _print_stats = True):
        if _print_stats:
            self.print_stats()
        
        self.create_body()
        
        self.write_file(filename) # 'MERGED_repo.tmx'

    def merge_repos(self, repo_root):
        start_time = time.time()
        print("------")
        for repo in os.listdir(repo_root):
            repo_path = os.path.join(repo_root, repo)
            if os.path.isdir(repo_path):
                save_path = os.path.join(repo_path, "DialogeOmegaT",'omegat','project_save.tmx')
                if os.path.isfile(save_path):
                    # parse_time = time.time()
                    self.parse(save_path)
                    print(os.path.basename(repo_path), "додано")
                    # print_time(parse_time, "Час:")

        print_time(start_time, "Загальний час:")            

    def merge_dir(self, directory):
        # start_time = time.time()
        print("------")
        for file in os.listdir(directory):
            file_path = str(os.path.join(directory, file))
            if file_path.endswith(".tmx"):
            # if check_ext(file_path, "tmx"):
                self.parse(file_path)
                print(os.path.basename(file_path), "додано")
                    
        # self.create('MERGED_dir.tmx', start_time)

    def merge_args(self, *tmx_files):
        # start_time = time.time()
        print("------")
        for file in tmx_files:
            if file.endswith(".tmx"):
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
            if not force:
                self.add_tu(tu)
            else:
                self.add_tu_force(tu)

    def create_body(self):
        for key in sorted(self._tu_dict.keys()):
            self.body.append(self._tu_dict[key].text())
        
        if self._alt_dict:
            for key in sorted(self._alt_dict.keys()):
                self.body.append(self._alt_dict[key].text())

    def print_stats(self):
        all_str = "Всього:\t" + str(len(self._tu_dict))
        diff_str = "Відмінностей: " + str(self._tu_dict.diff)
        replace_str = "Замін:\t" + str(self._tu_dict.replace)

        if self._alt_dict:
            all_str = f"Всього:\t{len(self._tu_dict) + len(self._alt_dict)} ({len(self._tu_dict)} + {len(self._alt_dict)})"
            if self._alt_dict.diff:
                diff_str = f"Відмінностей: {self._tu_dict.diff + self._alt_dict.diff} ({self._tu_dict.diff} + {self._alt_dict.diff})"
            if self._alt_dict.replace:
                replace_str = f"Замін:\t{self._tu_dict.replace + self._alt_dict.replace} ({self._tu_dict.replace} + {self._alt_dict.replace})"

        print("------")
        print(all_str)
        print(diff_str)
        print(replace_str)

    def write_file(self, tmx_file_path):
        # tmx_file_path = os.path.join(directory, 'MERGED.tmx')
        # tmx_file_path = 'MERGED.tmx'
        with open(tmx_file_path, 'w', encoding='utf-8') as file: # 'wb'
            xml_string = etree.tostring(self.root, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode()
            file.write(xml_string)
    
    def remove_newlines(self):
        tu_n = self._tu_dict.remove_newlines()
        n_str = "newlines removed: " + str(tu_n)

        tu_q = self._tu_dict.remove_quotes()
        q_str = "quotes removed: " + str(tu_q)

        tu_d = self._tu_dict.replace_four_dots()
        d_str = "dots removed: " + str(tu_d)

        if self._alt_dict:
            alt_n = self._alt_dict.remove_newlines()
            alt_q = self._alt_dict.remove_quotes()
            alt_d = self._alt_dict.replace_four_dots()

            if alt_n:
                n_str = "newlines removed: " + str(tu_n + alt_n) + " (" + str(tu_n) + " + " + str(alt_n) + ")"
            if alt_q:
                q_str = "quotes removed: " + str(tu_q + alt_q) + " (" + str(tu_q) + " + " + str(alt_q) + ")"
            if alt_d:
                d_str = "quotes removed: " + str(tu_d + d_str) + " (" + str(tu_d) + " + " + str(d_str) + ")"

        print("------")
        print(n_str + " segments")
        print(q_str + " segments")
        print(d_str + " segments")

    def print_notes(self):
        self._tu_dict.print_notes()
        self._alt_dict.print_notes()

# Виводить час, який пройшов зі start_time
def print_time(start_time, text):
    end_time = time.time()
    execution_time = end_time - start_time
    print(text, execution_time)

# Перевіряє розширення
# def check_ext(file_path : str, ext : str):
#     if os.path.isfile(file_path):
#         file_name, file_ext = os.path.splitext(file_path)
#         file_ext = file_ext.lstrip('.') # видаляє крапку
#         return file_ext == ext

