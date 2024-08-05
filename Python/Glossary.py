class Glossary:
    def __init__(self, txt_file = None):
        self.content = set()
        if txt_file:
            self.add_file(txt_file)

    def add_file(self, txt_file):
        with open(txt_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                line = tuple(line.strip().split('\t'))
                self.content.add(line)

    def add_line(self, key, value):
        line = (key, value) # tuple
        self.content.add(line)

    @staticmethod
    def get_str(line : tuple):
        line = '\t'.join(line) + '\n'
        return line

    def write(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            for line in sorted(self.content):
            # for line in self.content:
                file.write(Glossary.get_str(line))

    def diff(self, glossary : "Glossary"):
        # return self.content - glossary.content
        return self.content.difference(glossary.content)
    
    def update(self, glossary : "Glossary"):
        # self.content = self.content.union(glossary.content)
        self.content.update(glossary.content)

if __name__ == '__main__':
    gloss = Glossary("glossary\\glossary.txt")
    gloss.write("glossary\\new_glossary.txt")
