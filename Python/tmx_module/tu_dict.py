from datetime import datetime
from lxml import etree

class base_tu:
    def __init__(self, tu):
        self.tu = tu
    
    def text(self):
        return self.tu

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

    # ключем для base_tu є польський текст
    def get_key(self):
        return self.get_pl_text()

    def get_uk_seg(self):
        seg_uk = self.tu.find("./tuv[@lang='uk']/seg")
        return seg_uk

    def add_uk_text(self, text):
        seg_uk = self.get_uk_seg()
        seg_uk.text = text + seg_uk.text
        # seg_uk.text = etree.CDATA(text + seg_uk.text)

    def change_pl_text(self, text : str):
        seg_pl = self.tu.find("./tuv[@lang='pl']/seg")
        seg_pl.text = text

    def add_note(self, text : str):
        note = etree.SubElement(self.tu, "note")
        note.text = text

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

        return base_tu(tu)

    # @staticmethod
    def check_note(self):
        return self.tu.find("./note")

    def print_note(self):
        if self.check_note() is not None:
            print("------")
            tuv_uk = self.tu.find("./tuv[@lang='uk']")
            creationid = tuv_uk.attrib.get('creationid')
            changeid = tuv_uk.attrib.get('changeid')
            print(self.get_date().strftime("%d.%m.%y"))
            print(f"{creationid}, {changeid}:", self.tu.find("./note").text)
            print("pl:", self.get_pl_text())
            print("uk:", self.get_uk_text())

class prop_tu(base_tu):
    def __init__(self, tu):
        super().__init__(tu)

    def get_prop_id(self):
        file_text = self.tu.find("./prop[@type='file']").text
        id_text =   self.tu.find("./prop[@type='id']").text
        # if file_text and id_text:
        return (file_text, id_text)

    # ключем для prop_tu є id
    def get_key(self):
        return self.get_prop_id()

    def prop_equal(self, other_tu : 'prop_tu'):
        return self.get_prop_id() == other_tu.get_prop_id()

    @staticmethod
    def check_prop(tu):
        return tu.find("./prop")


class tu_dict:
    def __init__(self):
        self._tu_dict = {} # data

        # self.repeat = 0
        self.diff = 0
        self.replace = 0

    def __getitem__(self, key):
        return self._tu_dict[key]

    def __setitem__(self, key, tu):
        self._tu_dict[key] = tu

    def __delitem__(self, key):
        del self._tu_dict[key]

    def __bool__(self):
        return bool(self._tu_dict)
    
    def __len__(self):
        return len(self._tu_dict)

    # для оператора in
    def __contains__(self, key):
        return key in self._tu_dict # .keys()
    
    def contains(self, tu):
        return self.__contains__(tu)
    
    def keys(self):
        return self._tu_dict.keys()
    
    def values(self):
        return self._tu_dict.values()
    
    def pop(self, key):
        return self._tu_dict.pop(key, None)

    def replace_tu(self, tu : base_tu, force=False):
        key = tu.get_key()
        ex_tu = self._tu_dict[key]
        if not tu.equal_uk(ex_tu):
            self.diff += 1
            if not force:
                if (tu.get_date() > ex_tu.get_date()):
                    self._tu_dict[key] = tu
                    self.replace += 1
            else:
                self._tu_dict[key] = tu
                self.replace += 1

    def add(self, tu : base_tu, force=False):
        key = tu.get_key()
        if key not in self._tu_dict:
            self._tu_dict[key] = tu
        else:
            self.replace_tu(tu, force) # False as default

    def remove_newlines(self):
        return self.replace_symbol('\n')
    
    def replace_symbol(self, symbol, replacement=""):
        count = 0
        for key in self._tu_dict:
            uk_seg = self._tu_dict[key].get_uk_seg()
            if symbol in uk_seg.text:
                uk_seg.text = uk_seg.text.replace(symbol, replacement)
                count += 1
        return count
    
    def replace_four_dots(self):
        return self.replace_symbol("....", "...")

    # def remove_eight_spaces(self):
    #     return self.replace_symbol("        ")

    def remove_quotes(self):
        count = 0
        for key in self._tu_dict:
            uk_seg = self._tu_dict[key].get_uk_seg()
            if '\"' in uk_seg.text:
                self.detect_quotes(uk_seg)
                count += 1
        return count
    
    def detect_quotes(self, seg):
        count = seg.text.count('\"')
        print("------")
        print(f"{count} quotes")
        print(f"{seg.text}")
        if count > 1:
            seg.text = seg.text.replace('\"', "\'")
        else:
            seg.text = seg.text.replace('\"', "")

        print(f"{seg.text}")    # відображає вже замінений варіант, не враховує наявні '

    def print_notes(self):
        for tu in self._tu_dict.values():
            tu.print_note() # check_note inside

# # тест base_tu
# def run_tu_test():
#     tu = base_tu.create_tu("Польський текст", "Український текст")
#     tu.add_uk_text("[Додатковий текст]") # не використовувати <>
#     tu_2 = base_tu.create_tu("Żądło rzecznego krwiopijcy", "Жало річкового шершня", "Gliban")
#     tu_2.add_uk_text("[DEEPL]")

#     tmx_file = TMX_Merger()
#     tmx_file._tu_dict[tu.get_pl_text()] = tu
#     tmx_file._tu_dict[tu_2.get_pl_text()] = tu_2
#     tmx_file.create("tu_test.tmx")
