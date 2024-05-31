from lxml import etree
from datetime import datetime
import sys
import io
import os.path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

current_directory = os.path.dirname(os.path.abspath(__file__))
tmx_file = os.path.join(current_directory, "project_save_5.tmx")
root = etree.parse(tmx_file)

# root = etree.parse("2_Араксос_project_save.tmx")

# tu_elements = root.xpath("//tu")
# existing_tus = set()

# for tu in root.xpath("//tu"):
    # existing_tus.add(tu)

def create_body(root):
    body = etree.Element('body')

    for tu in root.xpath('//tu'):
        # tu_string = etree.tostring(tu)
        if tu not in body:
            # existing_tus.add(tu)
            body.append(tu)

    # Перетворення елементу body у рядок XML
    body_string = etree.tostring(body, pretty_print=True)
    print(body_string.decode())
    return body

# create_body(root)

def print_tuv_pl(root):
    for tuv in root.xpath("//tu/tuv[@lang='pl']"):
        tuv_string = etree.tostring(tuv, pretty_print=True)
        print(tuv_string.decode())
            
# print_tuv_pl(root)

def get_date(tu):
    tuv_uk = tu.find("./tuv[@lang='uk']")
    changedate_value = tuv_uk.attrib.get('changedate')
    date_time = datetime.strptime(changedate_value, "%Y%m%dT%H%M%SZ")
    return date_time
    
def get_pl_text(tu):
    pl_text = tu.find("./tuv[@lang='pl']/seg").text
    # print(text)
    return pl_text

# for tu in root.xpath("//tu"):
    # print(get_pl_text(tu))
    
def equal_uk(tu_1, tu_2):
    uk_1_text = tu_1.find("./tuv[@lang='uk']/seg").text
    uk_2_text = tu_2.find("./tuv[@lang='uk']/seg").text
    return uk_1_text == uk_2_text
    
def print_dates(root):
    for tu in root.xpath("//tu"):
        print(get_date(tu))
        
# print_dates(root)

def unique_pl_old(root):
    existing_tus = set()
    for tu in root.xpath("//tu"):
        if tu not in existing_tus:
            tu_text_pl = get_pl_text(tu)
            if existing_tus:
                for ex_tu in list(existing_tus):
                    ex_text_pl = get_pl_text(ex_tu)
                    if tu_text_pl != ex_text_pl:
                        existing_tus.add(tu)
            else:
                existing_tus.add(tu)
        
    return existing_tus
    
def unique_pl_new(root):
    tu_dict = {}
    repeat = 0
    replace = 0
    print("------")
    for tu in root.xpath("//tu"):
        # print(get_date(tu))
        tu_text_pl = get_pl_text(tu)
        if tu_text_pl not in tu_dict:
            tu_dict[tu_text_pl] = tu
            print("element edded", get_date(tu))
            print("------")
        else:
            ex_tu = tu_dict[tu_text_pl]
            repeat += 1
            if not equal_uk(tu, ex_tu):
                # print("tu\t", get_date(tu))
                # print("ex_tu\t", get_date(ex_tu))
                if (get_date(tu) > get_date(ex_tu)):
                    tu_dict[tu_text_pl] = tu
                    print(get_date(ex_tu), " replaced by ", get_date(tu))
                    replace += 1
                else:
                    print("received", get_date(ex_tu))
                print("------")
            else:
                print("already exists", get_date(ex_tu))
                print("------")
                
    print("len:\t", len(tu_dict))
    print("repeat:\t", repeat)
    print("replace:", replace)
    
    return tu_dict

# existing_tus = unique_pl_new(root)
# if not existing_tus:
    # print("existing_tus is empty")

# for tu in root.xpath("//tu"):
    # print(get_date(tu))
    # print(get_pl_text(tu))

print("__file__", __file__)
print("abspath", os.path.abspath(__file__))
current_directory = os.path.dirname(os.path.abspath(__file__))
print("dirname:", current_directory)
print("normpath:", os.path.normpath(current_directory))
print("join:", os.path.join(current_directory, 'MERGED.tmx'))
