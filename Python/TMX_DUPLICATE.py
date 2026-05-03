import os, io, sys, re
from TMX_Wrapper import TMX_Wrapper
from json_module.jsonFile import jsonFile

# шукає повторювані слова, які йдуть підряд,
# рядки, які починаються з малої букви,
# і рядки, які закінчуються на щось, окрім зазначених символів
class TMX_DUPLICATE(TMX_Wrapper):
    def __init__(self, tmx_file):
        super().__init__(tmx_file)
        self.duplicates = []
        self.lowercase = []
        self.invalid_end = []

    def find_all_with_json(self, pl_json : jsonFile):
        for pl_text in pl_json.values():
            if pl_text in self.tmx_file._tu_dict:
                uk_text = self.tmx_file._tu_dict[pl_text].get_uk_text()

                if uk_text[0].isalpha() and uk_text[0].islower():
                # if uk_text.startswith('c') or uk_text.startswith('с'):
                    self.lowercase.append(uk_text)

                if not uk_text.endswith((".", "!", "?", ")", ">", "\'", ":")): # or ("...." in uk_text) or ("*" in uk_text):
                    self.invalid_end.append(uk_text)

                words = TMX_DUPLICATE.get_words(uk_text)
                if TMX_DUPLICATE.is_duplicate(words):
                    self.duplicates.append(uk_text)

    def find_duplicates(self):
        for tu in self.tmx_file._tu_dict.values():
            text = tu.get_uk_text()
            words = TMX_DUPLICATE.get_words(text)
            if TMX_DUPLICATE.is_duplicate(words):
                self.duplicates.append(text)

    def write_duplicates(self):
        if self.duplicates or self.lowercase or self.invalid_end:
            path = os.path.join(os.path.dirname(self.filepath), 'duplicates.txt')

            with open(path, 'w', encoding="utf-8") as file:
                if self.duplicates:
                    file.write('------duplicates------\n')
                    for item in self.duplicates:
                        file.write(item + '\n')
                if self.lowercase:
                    file.write('------lowercase------\n')
                    for item in self.lowercase:
                        file.write(item + '\n')
                if self.invalid_end:
                    file.write('------invalid_end------\n')
                    for item in self.invalid_end:
                        file.write(item + '\n')

            print(f"В файл {path} записано:")
            print(f"{len(self.duplicates)} рядків з повторюваними підряд словами")
            print(f"{len(self.lowercase)} рядків з малої букви")
            print(f"{len(self.invalid_end)} рядків з невідповідними закінченнями")

        else:
            print("Список дублікатів пустий")

    @staticmethod
    def get_words(text : str):
        # ігнорує всі пунктуаційні символи
        clean_text = re.sub(r'[^a-zA-Zа-яА-ЯїЇєЄіІґҐ0-9 ]', '', text)
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

def run_json():
    print("Завантаження файлів...")
    archolos_edit = os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\omegat\project_save.tmx')
    duplicate = TMX_DUPLICATE(archolos_edit)
    pl_json = jsonFile()
    # Shift + Alt + ↓
    pl_json.load_loc(os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\source\pl\Scripts\Content\Story\Dialog_Mobsis'))
    pl_json.load_loc(os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\source\pl\Scripts\Content\Story\EventManager'))
    pl_json.load_loc(os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\source\pl\Scripts\Content\Story\Events'))
    pl_json.load_loc(os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\source\pl\Scripts\Content\Story\B_AssignAmbientInfos'))
    pl_json.load_loc(os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\source\pl\Scripts\Content\Story\B_Story'))
    pl_json.load_loc(os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\source\pl\Scripts\Content\Story\Cutscenes'))
    pl_json.load_loc(os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\source\pl\Scripts\Content\Story\Dialoge'))
    pl_json.load_file(os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\source\pl\Scripts\Content\Story\Log_Entries\LOG_Entries.d.json'))
    pl_json.load_file(os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\source\pl\Scripts\Content\Story\svm.d.json'))
    duplicate.find_all_with_json(pl_json)
    duplicate.write_duplicates()

# Запуск програми
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # print(TMX_DUPLICATE.get_words(r"234!@!%^&*()'Sdfsdfsf ';Erhhth@#$ 2*sdFsds![]{},...."))
    # print(TMX_DUPLICATE.get_words(r"ї2 Ліваіпв 34!@івлоіолва !%б^& Іі*()' фівдлф а'; валвава@#$ 2* вавап![]{} івваі ,.ґҐ. Ї.Єє.??????"))
    # run_duplicates()
    run_json()
