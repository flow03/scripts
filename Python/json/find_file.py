# import os
import sys
import io
from pathlib import Path

# def list_files(directory):
    # files = os.listdir(directory)
    # for file in files:
        # print(file)
        
def find_file(start_directory, filename):
    for file in Path(start_directory).rglob('*.json'):
        # print(file)
    
        if file.name == filename:
            # file_path = os.path.join(root, filename)
            print(f"Файл '{file}' знайдено")
            return file
    
    print(f"Файл '{filename}' не знайдено.")
    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Using: python script.py <folder_path> <filename>")
        sys.exit(1)
    else:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

        directory_path = sys.argv[1]
        # print("directory_param", directory_path)
        # directory_path = os.path.normpath(directory_path)
        # print("param_normpath", directory_path)
        # directory_path = "D:\Dropbox\Archolos\CoM_localization_repository\pl"
        # print("directory_win", directory_path)
        directory_path = Path("/d/Dropbox/Archolos/CoM_localization_repository/pl")
        print("directory_Path", directory_path)
        # directory_path = os.path.normpath(directory_path)
        # print("unix_normpath", directory_path)
        
        if not directory_path.exists():
            print(f"Шлях '{directory_path}' не знайдено.")
            sys.exit(1)
        # directory_path = os.path.normpath(directory_path)
        # print("directory_path", directory_path)
        # print()
        # list_files(directory_path)
        
        # Приклад використання
        # directory = "/d/Dropbox/Archolos/CoM_localization_repository/pl/Scripts/Content/Story/"
        filename = sys.argv[2]
        filename = "Mod_Text.d.json"

        find_file(directory_path, filename)

