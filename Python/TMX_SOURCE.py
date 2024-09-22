import os, io, sys
from TMX_Wrapper import TMX_Wrapper

# оновлює польські репліки на основі нових і старих сурсів у форматі json
class TMX_SOURCE(TMX_Wrapper):
    def __init__(self, tmx_file, source_old, source_new):
        super().__init__(tmx_file)
        self.source_old = TMX_Wrapper.get_json(source_old)
        # print("source_old:", len(self.source_old.data), "elements")
        self.source_new = TMX_Wrapper.get_json(source_new)
        # print("source_new:", len(self.source_new.data), "elements")
        # print("tmx_file:", len(self.tmx_file._tu_dict), "elements")

    def update(self):
        tmx_keys = self.tmx_file._tu_dict.keys()
        diff = 0
        replace = 0

        for key in self.source_new.keys():
            # TODO передбачає, що в обох словниках обов'язково співпадають усі ключі
            old_value = self.source_old[key]
            new_value = self.source_new[key]
            if new_value != old_value:
                diff += 1
                if old_value in tmx_keys: # значення json файлу це ключ для tmx файлу
                    tu = self.tmx_file._tu_dict.pop(old_value)
                    tu.change_pl_text(new_value)
                    note = self.create_note(old_value, new_value)
                    tu.add_note(note)
                    self.tmx_file._tu_dict[new_value] = tu
                    replace += 1
        
        print("Відмінностей:", diff)
        print("Замін:", replace)
        # print("tmx_file:", len(self.tmx_file._tu_dict), "elements")

        self.backup()
        self.create()

    def create_note(self, old_value, new_value):
        text = "[NEW_SOURCE]\n" + new_value + "\n[OLD_SOURCE]\n" + old_value
        return text

# Запуск програми
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    # archolos_edit = os.path.normpath(r'D:\Projects\scripts\Python\test\Archolos_edit_test.tmx')
    archolos_edit = os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\omegat\project_save.tmx')
    # source_old = os.path.normpath(r'D:\Archolos\Archolos_edit\DialogeOmegaT\source\pl')
    source_old = os.path.normpath(r'D:\Archolos\source_back\OLD_source\pl')
    source_new = os.path.normpath(r'D:\Dropbox\Archolos\CoM_localization_repository\pl')

    new_tmx = TMX_SOURCE(archolos_edit, source_old, source_new)
    new_tmx.update()
