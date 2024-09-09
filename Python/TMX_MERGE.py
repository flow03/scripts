import os
import sys
import io
from TMX_Wrapper import TMX_Wrapper

class TMX_MERGE(TMX_Wrapper):
    def __init__(self, tmx_file):
        super().__init__(tmx_file)

    def merge(self, repo_root):
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

def run_merge():
    archolos_edit = os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\omegat\project_save.tmx')
    repo_path = os.path.normpath(r'D:\Dropbox\Archolos\OmegaT')
    merger = TMX_MERGE(archolos_edit)
    merger.merge(repo_path)

def run_merge_dir(directory_path):
    archolos_edit = os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\omegat\project_save.tmx')
    merger = TMX_MERGE(archolos_edit)
    merger.merge_dir(directory_path)

# Запуск програми
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    run_merge()
    # run_merge_dir('1')