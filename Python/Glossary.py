class Glossary:
    def __init__(self, txt_file):
        self.content = []
        self.add(txt_file)

    def add(self, txt_file):
        with open(txt_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                # line = line.strip()
                # line = line.split('\t')
                line = tuple(line.strip().split('\t'))
                # print(line)
                if line not in self.content:
                    self.content.append(line)
        
        self.content.sort()

    def add_line(self, key, value):
        line = (key, value) # tuple
        if line not in self.content:
            self.content.append(line)

    def get_str(self, line : tuple):
        line = '\t'.join(line) + '\n'
        return line

    def write(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            for line in self.content:
                file.write(self.get_str(line))

if __name__ == '__main__':
    gloss = Glossary("glossary.txt")
    gloss.write("new_glossary.txt")
