import os, sys, io
from pathlib import Path

def find_file_os(start_dir, filename):
    # cycles = 0
    for root, dirs, files in os.walk(start_dir):
        # cycles += 1
        if filename in files:
            file_path = os.path.join(root, filename)
            # print(f"Циклів {cycles}")
            # print(f"Файл '{file_path}' знайдено")
            return file_path
    
    # print(f"Циклів {cycles}")
    # print(f"Файл '{filename}' не знайдено.")
    # sys.exit(1)
    return None

def find_file_Path(start_dir, filename):
    cycles = 0
    for file in Path(start_dir).rglob('*.json'):
        # print(file)
        cycles += 1
        if file.name == filename:
            print(f"Циклів Path {cycles}")
            print(f"Файл '{file}' знайдено")
            return file
            
    print(f"Циклів Path {cycles}")
    print(f"Файл '{filename}' не знайдено.")
    # sys.exit(1)
    return None

def check_path_os(path):
    directory_path = os.path.normpath(path)
    if os.path.exists(directory_path):
        # print(f"Шлях '{directory_path}' не знайдено.")
        # sys.exit(1)
        return directory_path
    else:
        # print(f"Шлях '{directory_path}'") 
        return None

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

