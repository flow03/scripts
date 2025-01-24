import os
import sys
import io
from TMX_Wrapper import TMX_Wrapper

# об'єднує усі сейви і перезаписує сейв у Archolos_edit
class TMX_MERGE(TMX_Wrapper):
    def __init__(self, tmx_file):
        super().__init__(tmx_file)

    def merge_repo(self, repo_root):
        if not os.path.isdir(repo_root):
            print(f"Теки \"{repo_root}\" не існує")
            exit(1)
            
        self.tmx_file.merge_repos(repo_root)
        self.tmx_file.print_stats()
        self.tmx_file.remove_newlines()

        print("------")
        self.backup()
        self.create()

    def merge_dir(self, directory):
        if not os.path.isdir(directory):
            print(f"Теки \"{directory}\" не існує")
            exit(1)
            
        self.tmx_file.merge_dir(directory)
        self.tmx_file.print_stats()
        self.tmx_file.remove_newlines()

        print("------")
        self.backup()
        self.create()

    def merge_file(self, file):
        if not os.path.isfile(file):
            # print(f"Файлу \"{file}\" не існує")
            exit(1)
            
        self.tmx_file.add_file(file)
        self.tmx_file.print_stats()
        self.tmx_file.remove_newlines()

        print("------")
        self.backup()
        self.create()

# об'єднує всі сейви у репозиторіях у вказаній теці і сейв Archolos_edit
def run_merge_repo():
    archolos_edit = os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\omegat\project_save.tmx')
    repo_path = os.path.normpath(r'D:\Dropbox\Archolos\OmegaT')
    merger = TMX_MERGE(archolos_edit)
    merger.merge_repo(repo_path)

# об'єднує tmx файли у вказаній теці з сейвом Archolos_edit
def run_merge_dir(directory_path):
    archolos_edit = os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\omegat\project_save.tmx')
    merger = TMX_MERGE(archolos_edit)
    merger.merge_dir(directory_path)

# об'єднує сейв Aedan і сейв Archolos_edit
def run_aedan():
    archolos_edit = os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\omegat\project_save.tmx')
    # aedan_save = os.path.normpath(r'D:\Dropbox\Archolos\OmegaT\Aedan_DialogeOmegaT_pl\DialogeOmegaT\omegat\project_save.tmx')
    all_save = os.path.normpath(r'D:\Dropbox\Archolos\OmegaT\Project_ALL\DialogeOmegaT\omegat\project_save.tmx')
    merger = TMX_MERGE(archolos_edit)
    merger.merge_file(all_save)

# Запуск програми
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # run_merge()
    # run_merge_dir('1')
    run_aedan()
