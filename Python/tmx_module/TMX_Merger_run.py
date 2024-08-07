import os
import sys
# import time
import io
from TMX_Merger import TMX_Merger, check_ext

# ----------------------------------------------------

def run_with_argv():
    if len(sys.argv) < 2:
        print("Використання:")
        print("python script.py <repositories>")
        print("python script.py <repositories> <add_tmx_file>")
        sys.exit(1)
    else:
        directory_path = sys.argv[1]
        directory_path = os.path.normpath(directory_path)
        merger = TMX_Merger()
        if len(sys.argv) == 3:
            add_file = sys.argv[2]
            if check_ext(add_file, "tmx"): # isfile
                merger.add_tmx(add_file)

        if os.path.isdir(directory_path):
            merger.merge_repos(directory_path)
            merger.create('MERGED_repo.tmx')
        # else:
        #     print(directory_path, "не є директорією")

def run_dir(directory_path):
    if os.path.isdir(directory_path):
        merger = TMX_Merger()
        merger.merge_dir(directory_path)
        merger.create('MERGED_dir.tmx')

def run_Dialoges():
    repositories_path = os.path.normpath(r'D:\Dropbox\Archolos\OmegaT')
    tmx_path = os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\omegat\project_save.tmx')
    name = os.path.join('tmx', 'project_save.tmx')
    if os.path.isdir(repositories_path):
        merger = TMX_Merger(tmx_path)
        merger.merge_repos(repositories_path)
        merger.remove_newlines()
        merger.create(name)
        print("Об\'єднаний", name, "успішно створено")

def run_Archolos():
    archolos_work = os.path.normpath(r"D:\Archolos\Archolos_work\ArcholosOmegaT\omegat\project_save.tmx")
    aedan_a = os.path.normpath(r"D:\Dropbox\Archolos\OmegaT_a\Aedan_ArcholosOmegaT_pl\ArcholosOmegaT\omegat\project_save.tmx")
    name = os.path.join('tmx', 'project_save_a.tmx')
    merger = TMX_Merger(archolos_work)
    merger.add_tmx(aedan_a)
    merger.remove_newlines()
    merger.create(name)
    print("Об\'єднаний", name, "успішно створено (ArcholosOmegaT)")

# Запуск програми
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # run_Dialoges()
    run_Archolos()
