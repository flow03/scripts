from Glossary import Glossary
import os

class Glossary_sync:
    def __init__(self, filename = "glossary.txt"):
        self.filename = filename
        origin_path = os.path.join(r"D:\Archolos\Archolos_edit\DialogeOmegaT\glossary", self.filename)
        self.origin = Glossary(origin_path)

        self.pathes = self.get_pathes()
        # for path in self.pathes:
        #     print(path)
        self.glossaries = {}
        self.add_glossaries()
        # for key in self.glossaries.keys():
        #     print(key)

    def add_glossaries(self):
        for path in self.pathes:
            if os.path.isdir(path):
                glossary_path = os.path.join(path, self.filename)
                self.add_glossary(glossary_path)

    # повертає четверту частину шляху з кінця
    # @staticmethod
    def get_name(self, path : str):
        parts = os.path.normpath(path).split(os.sep)
        if len(parts) >= 4:
            return parts[-4]

    def add_glossary(self, glossary_path):
        if os.path.isfile(glossary_path):
            name = self.get_name(glossary_path)
            if not name:
                name = glossary_path

            self.glossaries[name] = Glossary(glossary_path)

    # виводить на екран різницю між усіма глосаріями і origin, або навпаки
    def print_diff(self, reverse=False):
        for name, glossary in self.glossaries.items():
            if not reverse:
                # всі глосарії порівнюються з origin
                diff = glossary.diff(self.origin)
            else:
                # origin порівнюється з усіма глосаріями 
                diff = self.origin.diff(glossary)

            if diff:
                print()
                print(" ", name)
                for line in diff:
                    # print(f"   {key}\t{value}")
                    print(Glossary.get_str(line), end="") # рядок вже з \n

    # об'єднує усі глосарії в один
    def create(self):
        for glossary in self.glossaries.values():
            self.origin.update(glossary)

    # перезаписує УСІ глосарії за вказаними шляхами
    def rewrite(self):
        for path in self.pathes:
            filepath = os.path.join(path, self.filename)
            self.origin.write(filepath)
            print(filepath, "створено")

    # повертає шляхи до усіх тек з глосаріями
    def get_pathes(self):
        pathes = []
        pathes.append(r"D:\Archolos\Archolos_edit\DialogeOmegaT\glossary")
        pathes.append(r"D:\Archolos\Archolos_work\ArcholosOmegaT\glossary")
        pathes.extend(self.get_repo_pathes(r"D:\Dropbox\Archolos\OmegaT", "DialogeOmegaT")) # +=
        pathes.extend(self.get_repo_pathes(r"D:\Dropbox\Archolos\OmegaT_a", "ArcholosOmegaT")) # +=

        return pathes
    
    # повертає шляхи до усіх тек з глосаріями у вказаному репозиторії
    def get_repo_pathes(self, repo, folder = "DialogeOmegaT"):
        pathes = []
        for name in os.listdir(repo):
            glossary_path = os.path.join(repo, name, folder, "glossary")
            if os.path.isdir(glossary_path):
                pathes.append(glossary_path)

        return pathes

if __name__ == '__main__':
    sync = Glossary_sync() # "names.txt" "Items.txt"
    sync.print_diff()
    # name = os.path.join("glossary_test", "glossary.txt")
    # sync.create()
    # sync.rewrite()
