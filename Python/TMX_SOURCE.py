import os, io, sys
from TMX_Wrapper import TMX_Wrapper

# оновлює польські репліки на основі нових і старих сурсів у форматі json
class TMX_SOURCE(TMX_Wrapper):
    def __init__(self, tmx_file, source_old, source_new):
        super().__init__(tmx_file)
        self.source_old = TMX_Wrapper.get_json(source_old)
        print("source_old:", len(self.source_old.data), "elements")
        self.source_new = TMX_Wrapper.get_json(source_new)
        print("source_new:", len(self.source_new.data), "elements")

def update():
    pass

# Запуск програми
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    archolos_edit = os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\omegat\project_save.tmx')
    source_old = os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\source\pl')
    source_new = os.path.normpath(r'D:\Dropbox\Archolos\CoM_localization_repository\pl')

    new_tmx = TMX_SOURCE(archolos_edit, source_old, source_new)
