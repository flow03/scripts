import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def list_files(directory):
    files = os.listdir(directory)
    for file in files:
        print(file)
        
def find_file(start_dir, filename):
    for root, dirs, files in os.walk(start_dir):
        if filename in files:
            # print("Файл знайдено!")
            return os.path.join(root, filename)
    return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Using: python script.py <folder_path>")
        sys.exit(1)
    else:
        directory_path = sys.argv[1]
        if not os.path.exists(directory_path):
            print(f"Шлях '{directory_path}' не знайдено.")
            sys.exit(1)
        directory_path = os.path.normpath(directory_path)
        print("directory_path", directory_path)
        print()
        # list_files(directory_path)
        
        # Приклад використання
        # directory = "/d/Dropbox/Archolos/CoM_localization_repository/pl/Scripts/Content/Story/"
        file_to_find = "Mod_Text.d.json"

        result = find_file(directory_path, file_to_find)
        if result:
            print(f"Файл '{file_to_find}' знайдено за наступним шляхом:")
            print(result)
        else:
            print(f"Файл '{file_to_find}' не знайдено.")

