import os
import sys
# import time
import io
from TMX_Merger import TMX_Merger, check_ext

# def get_date(tu):
#     tuv_uk = tu.find("./tuv[@lang='uk']")
#     changedate_value = tuv_uk.attrib.get('changedate')
#     date_time = datetime.strptime(changedate_value, "%Y%m%dT%H%M%SZ")
#     return date_time
    
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

# ----------------------------------------------------

def run_with_argv():
    if len(sys.argv) < 2:
        print("Використання: python script.py <directory_path> <tmx_file>")
        sys.exit(1)
    else:
        directory_path = sys.argv[1]
        directory_path = os.path.normpath(directory_path)
        merger = TMX_Merger()
        if len(sys.argv) == 3:
            add_file = sys.argv[2]
            if check_ext(add_file, "tmx"):
                # print(add_file, " має розширення tmx")
                merger.add_tmx(add_file)

        merger.run(directory_path)

def run(directory_path):
    # print("Програма запущена")
    merger = TMX_Merger()
    merger.run(directory_path)

# Запуск програми
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    run_with_argv()
    # run('D:\Dropbox\Archolos\OmegaT')
    # print("------")
