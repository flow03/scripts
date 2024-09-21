import os, io, sys
from shutil import copy
from TMX_Wrapper import TMX_Wrapper

# перезаписує усі сейви сейвом з Archolos_edit
class TMX_REPLACE(TMX_Wrapper):
    def __init__(self, tmx_file):
        super().__init__(tmx_file)

    def replace(self, repo_root):
        if not os.path.isdir(repo_root):
            print(f"Теки \"{repo_root}\" не існує")
            exit(1)

        for repo in os.listdir(repo_root):
            save_path = os.path.join(repo_root, repo, 'DialogeOmegaT','omegat','project_save.tmx')
            print(os.path.basename(repo))
            if os.path.isfile(save_path):
                self.backup(save_path)
                copy(self.filepath, save_path)
                print("project_save.tmx перезаписано")
            else:
                print(f"Відсутній файл project_save.tmx")
                copy(self.filepath, save_path)
                print("project_save.tmx створено")
            print()

def run_replace():
    archolos_edit = os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\omegat\project_save.tmx')
    repo_path = os.path.normpath(r'D:\Dropbox\Archolos\OmegaT')
    merger = TMX_REPLACE(archolos_edit)
    merger.replace(repo_path)

def run_replace_test():
    archolos_edit = os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\omegat\project_save.tmx')
    repo_test = os.path.normpath(r"D:\Archolos\Archolos_test\Test_repos")
    merger = TMX_REPLACE(archolos_edit)
    merger.replace(repo_test)

# Запуск програми
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    run_replace()
    # run_replace_test()
