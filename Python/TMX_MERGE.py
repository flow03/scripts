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
            
        folder = TMX_Wrapper.get_folder(self.filepath)
        self.tmx_file.merge_repos(repo_root, folder)
        self.tmx_file.print_stats()
        self.tmx_file.remove_newlines()

        print("------")
        self.backup()
        self.create()

def run_repo_Dialoge():
    archolos_edit = os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\omegat\project_save.tmx')
    repo_path = os.path.normpath(r'D:\Dropbox\Archolos\OmegaT')
    merger = TMX_MERGE(archolos_edit)
    # merger.backup()
    merger.merge(repo_path)

def run_repo_Archolos():
    archolos_work = os.path.normpath(r"D:\Archolos\Archolos_work\ArcholosOmegaT\omegat\project_save.tmx")
    repo_path = os.path.normpath(r"D:\Dropbox\Archolos\OmegaT_a")
    merger = TMX_MERGE(archolos_work)
    # merger.backup()
    merger.merge(repo_path)

# Запуск програми
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    if "-a" in sys.argv:
        run_repo_Archolos()
    else:
        run_repo_Dialoge()
