import os
import sys
# import time
import io
from TMX_Merger import TMX_Merger, check_ext

# ----------------------------------------------------

def get_name(path : str):
    parts = os.path.normpath(path).split(os.sep)
    if len(parts) >= 4:
        return parts[-4]

def run_dir(directory_path):
    if os.path.isdir(directory_path):
        merger = TMX_Merger()
        merger.merge_dir(directory_path)
        # merger.print_stats()
        merger.remove_newlines()

        name = "MERGED_dir.tmx"
        merger.create(name)
        print("------")
        print(name, "створено")
    else:
        print(f"Теки \"{directory_path}\" не існує")

def run_file(file_path):
    if os.path.isfile(file_path):
        merger = TMX_Merger(file_path)
        # merger.merge_dir(directory_path)
        # merger.print_stats()
        merger.remove_newlines()

        name = "FILE.tmx"
        merger.create(name)
        print("------")
        print(name, "створено")
    else:
        print(f"Файлу \"{file_path}\" не існує")

def run_Dialoges():
    archolos_edit = os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\omegat\project_save.tmx')
    repositories_path = os.path.normpath(r'D:\Dropbox\Archolos\OmegaT')
    name = os.path.join('tmx', 'project_save.tmx')
    if os.path.isdir(repositories_path):
        merger = TMX_Merger(archolos_edit)
        merger.merge_repos(repositories_path)
        merger.remove_newlines()
        merger.create(name)
        print("Об\'єднаний", name, "успішно створено")

def run_Archolos():
    archolos_work = os.path.normpath(r"D:\Archolos\Archolos_work\ArcholosOmegaT\omegat\project_save.tmx")
    aedan_a = os.path.normpath(r"D:\Dropbox\Archolos\OmegaT_a\Aedan_ArcholosOmegaT_pl\ArcholosOmegaT\omegat\project_save.tmx")
    name = os.path.join('tmx', 'project_save_a.tmx')
    if os.path.exists(aedan_a):
        merger = TMX_Merger(archolos_work)
        merger.add_tmx(aedan_a)
        merger.remove_newlines()
        merger.create(name)
        print("Об\'єднаний", name, "успішно створено (ArcholosOmegaT)")
    else:
        print(aedan_a, "не існує (ArcholosOmegaT)")

def run_repo(tmx_path, repo_path, folder = "DialogeOmegaT"):
    if not os.path.isfile(tmx_path):
        print(f"Файлу \"{tmx_path}\" не існує")
        exit(1)
    elif not os.path.isdir(repo_path):
        print(f"Теки \"{repo_path}\" не існує")
        exit(1)
        
    merger = TMX_Merger(tmx_path)
    merger.merge_repos(repo_path, folder)
    merger.remove_newlines()

    name = os.path.join('tmx', 'project_save (' + get_name(tmx_path) + ').tmx')
    merger.create(name)
    print("Об\'єднаний", name, "успішно створено")

# Запуск програми
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    run_dir("1")
    # run_file("project_save.tmx")
