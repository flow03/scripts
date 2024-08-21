import os, io, sys
from shutil import copy
from TMX_Wrapper import TMX_Wrapper

class TMX_REPLACE(TMX_Wrapper):
    def __init__(self, tmx_file):
        super().__init__(tmx_file)

    # def copy(self, filepath):
    #     if os.path.isfile(filepath):
    #         copy(self.filepath, filepath) # перезаписує файл, якщо такий є

    def replace(self, repo_root):
        if not os.path.isdir(repo_root):
            print(f"Теки \"{repo_root}\" не існує")
            exit(1)

        folder = TMX_Wrapper.get_folder(self.filepath)
        for repo in os.listdir(repo_root):
            save_path = os.path.join(repo_root, repo, folder,'omegat','project_save.tmx')
            print(os.path.basename(repo))
            if os.path.isfile(save_path):
                self.backup(save_path)
                copy(self.filepath, save_path)
                print("project_save.tmx перезаписано")
            else:
                filename = os.path.join(folder, 'omegat', 'project_save.tmx')
                print(f"Відсутній файл {filename}")
            print()

def run_repo_Dialoge():
    archolos_edit = os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\omegat\project_save.tmx')
    repo_path = os.path.normpath(r'D:\Dropbox\Archolos\OmegaT')
    merger = TMX_REPLACE(archolos_edit)
    merger.replace(repo_path)

def run_repo_Archolos():
    archolos_work = os.path.normpath(r"D:\Archolos\Archolos_work\ArcholosOmegaT\omegat\project_save.tmx")
    repo_path = os.path.normpath(r"D:\Dropbox\Archolos\OmegaT_a")
    merger = TMX_REPLACE(archolos_work)
    # merger.backup()
    merger.replace(repo_path)

def run_repo_test():
    archolos_edit = os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\omegat\project_save.tmx')
    repo_test = os.path.normpath(r"D:\Archolos\Archolos_test\Test_repos")
    merger = TMX_REPLACE(archolos_edit)
    merger.replace(repo_test)

# Запуск програми
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # run_repo_test()
    
    if "-a" in sys.argv:
        run_repo_Archolos()
    else:
        run_repo_Dialoge()
