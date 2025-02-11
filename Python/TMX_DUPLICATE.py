import os, io, sys, re
from TMX_Wrapper import TMX_Wrapper

# оновлює польські репліки на основі нових і старих сурсів у форматі json
class TMX_DUPLICATE(TMX_Wrapper):
    def __init__(self, tmx_file):
        super().__init__(tmx_file)
        self.duplicates = []

    def find_duplicates(self):
        for tu in self.tmx_file._tu_dict.values():
            text = tu.get_uk_text()
            words = TMX_DUPLICATE.get_words(text)
            if TMX_DUPLICATE.is_duplicate(words):
                self.duplicates.append(text)

    def write_duplicates(self):
        if self.duplicates:
            path = os.path.join(os.path.dirname(self.filepath), 'duplicates.txt')

            with open(path, 'w') as file:
                for item in self.duplicates:
                    file.write(item + '\n')

            print(f"В файл {path} записано {len(self.duplicates)} елементів")
        else:
            print("Список дублікатів пустий")

    @staticmethod
    def get_words(text : str):
         clean_text = re.sub(r'[^a-zA-Zа-яА-ЯїЇєЄіІґҐ ]', '', text)
         return clean_text.split()
    
    @staticmethod
    def is_duplicate(words : list):
        if len(words) > 1:
            for i in range(len(words) - 1):
                if words[i] == words[i + 1]:
                    return True

def run_duplicates():
    archolos_edit = os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\omegat\project_save.tmx')
    duplicate = TMX_DUPLICATE(archolos_edit)
    duplicate.find_duplicates()
    duplicate.write_duplicates()

# Запуск програми
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # print(TMX_DUPLICATE.get_words(r"234!@!%^&*()'Sdfsdfsf ';Erhhth@#$ 2*sdFsds![]{},...."))
    # print(TMX_DUPLICATE.get_words(r"ї2 Ліваіпв 34!@івлоіолва !%б^& Іі*()' фівдлф а'; валвава@#$ 2* вавап![]{} івваі ,.ґҐ. Ї.Єє.??????"))
    run_duplicates()
