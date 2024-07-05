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

def run_repos():
    repositories_path = r'D:\Dropbox\Archolos\OmegaT'
    if os.path.isdir(repositories_path):
        merger = TMX_Merger()
        merger.merge_repos(repositories_path)
        merger.force_add_tmx(r'D:\Archolos_edit\DialogeOmegaT\omegat\project_save.tmx')
        merger.create('MERGED_repo.tmx')

def run_dir(directory_path):
    if os.path.isdir(directory_path):
        merger = TMX_Merger()
        merger.merge_dir(directory_path)
        merger.create('MERGED_dir.tmx')

def run_args(*args):
    merger = TMX_Merger()
    merger.merge_args(*args)
    merger.create('MERGED_args.tmx')

# Запуск програми
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # run_with_argv()
    run_repos()
    # run_dir('merge')
    # run_dir('files')
    # run_args("fiercepretzel_save.tmx")
    # print("------")py 
