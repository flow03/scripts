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

def merge_tmx_files(directory):
    
    root = etree.Element('tmx')
    header = None
    body = etree.SubElement(root, 'body')

    tu_dict = {}
    repeat = 0
    replace = 0
    print("------")
    
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('project_save.tmx'):
                start_time = time.time()
                tree = etree.parse(os.path.join(dirpath, filename))
                # ------
                if header is None:
                    header = tree.find('header')
                    root.insert(0, header)
                # ------
                for tu in tree.xpath("//tu"):
                    tu_text_pl = get_pl_text(tu)
                    if tu_text_pl not in tu_dict:
                        tu_dict[tu_text_pl] = tu
                    else:
                        ex_tu = tu_dict[tu_text_pl]
                        repeat += 1
                        if not equal_uk(tu, ex_tu):
                            if (get_date(tu) > get_date(ex_tu)):
                                tu_dict[tu_text_pl] = tu
                                replace += 1
                # ------                
                # print(os.path.abspath(filename), ' appended')
                print(os.path.join(dirpath, filename), "додано")
                print_time(start_time, "Час:")

                
    print("------")
    print("Всього:\t", len(tu_dict))
    print("Повторів:", repeat)
    print("Замін:\t", replace)
    
    for key in sorted(tu_dict.keys()):
        body.append(tu_dict[key])
    
    # merged_tmx_path = os.path.join(directory, 'MERGED.tmx')
    merged_tmx_path = 'MERGED.tmx'
    with open(merged_tmx_path, 'wb') as f:
        f.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8'))

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# if __name__ == "__main__":
    # if len(sys.argv) != 2:
        # print("Using: python script.py <folder_path>")
        # sys.exit(1)
    # else:
        # directory_path = sys.argv[1]
        # directory_path = os.path.normpath(directory_path)
        # directory_path = directory_path.rstrip(os.path.sep)
        # print("directory_path", directory_path)
        # merge_tmx_files(directory_path)
start_time = time.time()
# print("Програма запущена")
merge_tmx_files('D:/Dropbox/Archolos/OmegaT')
print_time(start_time, "Час виконання:")
