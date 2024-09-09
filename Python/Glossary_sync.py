from Glossary import Glossary
import os

class Glossary_sync:
    def __init__(self, filename = "glossary.txt"):
        self.glossaries = {}

        pathes = Glossary_sync.get_pathes_test()
        # for path in pathes:
        #     print(path)
        self.add_glossaries(pathes, filename)
        # print()
        # for key in self.glossaries.keys():
        #     print(key)

    def add_glossaries(self, pathes, filename):
        for path in pathes:
            if os.path.isdir(path):
                glossary_path = os.path.join(path, filename)
                self.add_glossary(glossary_path)

    def add_glossary(self, glossary_path):
        if os.path.isfile(glossary_path):
            self.glossaries[glossary_path] = Glossary(glossary_path)

    # повертає четверту частину шляху з кінця
    @staticmethod
    def get_name(path : str):
        parts = os.path.normpath(path).split(os.sep)
        if len(parts) >= 4:
            return parts[-4]
        
    # виводить на екран різницю між усіма глосаріями
    def print_diff(self):
        unique_values = {}

        for path, glossary in self.glossaries.items():
            others = Glossary()

            # Додаємо всі інші глосарії, окрім поточного
            for p, gl in self.glossaries.items():
                if p != path:
                    others.update(gl)
            
            # Віднімаємо від поточного значення усіх інших глосаріїв
            # diff = glossary - others
            diff = glossary.diff(others)
            if diff:
                name = Glossary_sync.get_name(path)
                unique_values[name] = diff

        for name, diff in unique_values.items():
            print(" ", name)
            for line in diff:
                # print(f"   {key}\t{value}")
                print(Glossary.get_str(line), end="") # рядок вже з \n
            print()

    # об'єднує усі глосарії в один
    def merge(self):
        merged = Glossary()
        for glossary in self.glossaries.values():
            merged.update(glossary)

        return merged

    # перезаписує УСІ додані глосарії
    def sync(self):
        merged = self.merge()
        for path in self.glossaries.keys():
            # filepath = os.path.join(path, self.filename)
            merged.write(path)
            print(path, "створено")

    # повертає шляхи до усіх тек з глосаріями
    @staticmethod
    def get_pathes():
        pathes = []
        pathes.append(r"D:\Archolos\Archolos_edit\DialogeOmegaT\glossary")
        pathes.extend(Glossary_sync.get_repo_pathes(r"D:\Dropbox\Archolos\OmegaT")) # +=

        return pathes
    
    @staticmethod
    def get_pathes_test():
        return Glossary_sync.get_repo_pathes(r"D:\Archolos\Archolos_test\Test_repos")
    
    # повертає шляхи до усіх тек з глосаріями у вказаному репозиторії
    @staticmethod
    def get_repo_pathes(repo):
        pathes = []
        for name in os.listdir(repo):
            glossary_path = os.path.join(repo, name, "DialogeOmegaT", "glossary")
            if os.path.isdir(glossary_path):
                pathes.append(glossary_path)

        return pathes

if __name__ == '__main__':
    sync = Glossary_sync("glossary.txt") # "names.txt" "Items.txt"
    sync.print_diff()
    # sync.sync()
