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

    if "-a" in sys.argv:
        archolos_work = os.path.normpath(r"D:\Archolos\Archolos_work\ArcholosOmegaT\omegat\project_save.tmx")
        repo_path = os.path.normpath(r"D:\Dropbox\Archolos\OmegaT_a")
        run_repo(archolos_work, repo_path, folder = "ArcholosOmegaT")
    else:
        archolos_edit = os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\omegat\project_save.tmx')
        repo_path = os.path.normpath(r'D:\Dropbox\Archolos\OmegaT')
        run_repo(archolos_edit, repo_path)
