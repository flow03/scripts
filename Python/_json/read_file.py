import os
import io
import sys

def read_directory(path):
    # Перевірка чи існує вказаний шлях
    if not os.path.exists(path):
        print(f"Шлях '{path}' не існує.")
        return # повертає None
    else:
        print(f"Шлях '{path}' існує.")
        
    # Виведення вмісту теки
    # print(f"Вміст теки {path}:")
    # with os.scandir(path) as entries:
        # for entry in entries:
            # print(entry.name)

def read_file(file_path):
    # Читання файлу
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Перший рядок - шлях до теки
    directory_path = lines[0].strip()
    read_directory(directory_path)
    
    # Другий рядок - масив рядків, розділених пробілом
    string_array = lines[1].strip()
    if "," in string_array:
        string_array = string_array.replace(",", "")
    string_array = string_array.split(" ")
    print("Масив рядків:", string_array)
    
    # Читання пар "назва файлу і ключ"
    for line in lines[2:]:
        line = line.strip()
        if not line.startswith("#"):
            filename, key = line.split()
            print(f"Назва файлу: {filename}, Ключ: {key}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Using: python script.py <filename.txt>")
        sys.exit(1)
    else:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') # не більше одного разу
        # filename = sys.argv[1]
        read_file(sys.argv[1])
        