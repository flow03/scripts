from Glossary import Glossary
import os

class Glossary_sync:
    def __init__(self):
        self.origin_path = r"D:\Archolos_edit\DialogeOmegaT\glossary\glossary.txt"
        self.origin = Glossary(self.origin_path)
        self.glossaries = {}
        self.pathes = []

        # repo = r"D:\Archolos_test\Test_repos"
        repo = r"D:\Dropbox\Archolos\OmegaT"
        self.set_glossaries(repo)

    def set_glossaries(self, repo):
        for name in os.listdir(repo):
            repo_path = os.path.join(repo, name)
            if os.path.isdir(repo_path):
                glossary_path = os.path.join(repo_path, r"DialogeOmegaT\glossary\glossary.txt")
                if os.path.isfile(glossary_path):
                    self.glossaries[name] = Glossary(glossary_path)
                    self.pathes.append(glossary_path)

    def print_diff(self, reverse=False):
        for name, glossary in self.glossaries.items():
            if not reverse:
                diff = glossary.diff(self.origin)
            else:
                diff = self.origin.diff(glossary)

            if diff:
                print()
                print(" ", name)
                for line in diff:
                    # print(f"   {key}\t{value}")
                    print(Glossary.get_str(line), end="") # рядок вже з \n

    def create(self):
        for glossary in self.glossaries.values():
            self.origin.add_glossary(glossary)

        # self.origin.write(filename)
        # print(filename, "створено")

    def rewrite(self):
        self.origin.write(self.origin_path)
        print(self.origin_path, "створено")

        for path in self.pathes:
            self.origin.write(path)
            print(path, "створено")

    # def write(self, filename):
    #     self.origin.write(filename)

if __name__ == '__main__':
    sync = Glossary_sync()
    sync.print_diff()
    # name = os.path.join("glossary_test", "glossary.txt")
    sync.create()
    sync.rewrite()
