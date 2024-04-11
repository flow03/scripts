import os
import sys
from lxml import etree
from datetime import datetime
import time
import io

def print_time(start_time, text):
    end_time = time.time()
    execution_time = end_time - start_time
    print(text, execution_time)

def get_date(tu):
    tuv_uk = tu.find("./tuv[@lang='uk']")
    changedate_value = tuv_uk.attrib.get('changedate')
    date_time = datetime.strptime(changedate_value, "%Y%m%dT%H%M%SZ")
    return date_time
    
def get_pl_text(tu):
    pl_text = tu.find("./tuv[@lang='pl']/seg").text
    return pl_text
    
def equal_uk(tu_1, tu_2):
    uk_1_text = tu_1.find("./tuv[@lang='uk']/seg").text
    uk_2_text = tu_2.find("./tuv[@lang='uk']/seg").text
    return uk_1_text == uk_2_text

# def prop_equal_file(tu_1, tu_2):
    # file_1_text = tu_1.find("./prop[@type='file']").text
    # file_2_text = tu_2.find("./prop[@type='file']").text
    # return file_1_text == file_2_text    

# def prop_equal_id(tu_1, tu_2):
    # id_1_text = tu_1.find("./prop[@type='id]").text
    # id_2_text = tu_2.find("./prop[@type='id]").text
    # return id_1_text == id_2_text    

def get_prop_id(tu):
    file_text = tu.find("./prop[@type='file']").text
    id_text =   tu.find("./prop[@type='id']").text
    # if file_text and id_text:
    return (file_text, id_text)
    # else:
        # print(f"У даного tu '{get_pl_text(tu)}' відсутній prop_id")
        # return None

def prop_equal(tu_1, tu_2):
    # return prop_equal_file(tu_1, tu_2) and prop_equal_id(tu_1, tu_2)
    return get_prop_id(tu_1) == get_prop_id(tu_2)

def check_prop(tu):
    return tu.find("./prop")

def replace_tu(tu, tu_dict, key):
    # key = get_pl_text(tu)
    ex_tu = tu_dict[key]
    if not equal_uk(tu, ex_tu):
        if (get_date(tu) > get_date(ex_tu)):
            tu_dict[key] = tu
            # print(f"{get_date(ex_tu)} замінено на {get_date(tu)}")
            return 1 # replace
        # else:
            # print(f"{get_date(ex_tu)} залишено, натомість {get_date(tu)}")
    return 0

def merge_tmx_files(directory):
    
    root = etree.Element('tmx')
    header = None
    body = etree.SubElement(root, 'body')

    tu_dict = {}    # Default translations
    alt_dict = {}   # Alternative translations
    repeat = 0
    alt_repeat = 0
    replace = 0
    print("------")
    
    # for dirpath, dirnames, filenames in os.walk(directory):
        # for filename in filenames:
            # if filename.endswith('project_save.tmx'):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            start_time = time.time()
            save_path = os.path.join(item_path, 'DialogeOmegaT\omegat\project_save.tmx')        
            # tree = etree.parse(os.path.join(dirpath, filename))
            # print(save_path)
            # if os.path.exists(save_path):
                # print("Файл існує!")
            # print_time(start_time, "Час пошуку:")
            # '''
            tree = etree.parse(save_path)
            # ------
            if header is None:
                header = tree.find('header')
                root.insert(0, header)
            # ------
            for tu in tree.xpath("//tu"):
                if check_prop(tu) is None:
                    tu_text_pl = get_pl_text(tu)
                    if tu_text_pl not in tu_dict:
                        tu_dict[tu_text_pl] = tu
                    else:
                        repeat += 1
                        replace += replace_tu(tu, tu_dict, tu_text_pl)
                else: # prop
                    # print(f"prop '{get_pl_text(tu)}' знайдено")
                    prop_id = get_prop_id(tu)
                    if prop_id not in alt_dict:
                        alt_dict[prop_id] = tu
                    else:
                        alt_repeat += 1
                        replace += replace_tu(tu, alt_dict, prop_id)
            # ------                
            print(save_path, "додано")
            print_time(start_time, "Час:")
                
    print("------")
    if alt_dict:
        print(f"Всього:\t {len(tu_dict) + len(alt_dict)} ({len(tu_dict)} + {len(alt_dict)})")
    else:
        print("Всього:\t", len(tu_dict))
    print("Повторів:", repeat)
    print("Альтернативних повторів:", alt_repeat)
    print("Замін:\t", replace)
    
    for key in sorted(tu_dict.keys()):
        body.append(tu_dict[key])
    
    if alt_dict:
        for key in sorted(alt_dict.keys()):
            body.append(alt_dict[key])
    
    # merged_tmx_path = os.path.join(directory, 'MERGED.tmx')
    merged_tmx_path = 'MERGED.tmx'
    with open(merged_tmx_path, 'wb') as f:
        f.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
    # '''
    
def run_with_argv():
    if len(sys.argv) != 2:
        print("Використання: python script.py <folder_path>")
        sys.exit(1)
    else:
        directory_path = sys.argv[1]
        directory_path = os.path.normpath(directory_path)
        # directory_path = directory_path.rstrip(os.path.sep)
        print("Шлях", directory_path)
        start_time = time.time()
        merge_tmx_files(directory_path)
        print_time(start_time, "Час виконання:")

def run(path):
    start_time = time.time()
    print("Програма запущена")
    merge_tmx_files(path)
    print_time(start_time, "Час виконання:")

# Запуск програми
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # run_with_argv()
    run('C:/Users/Рома/Dropbox/Archolos/OmegaT')
