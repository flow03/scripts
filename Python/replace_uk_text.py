from tmx_module.TMX_Merger import TMX_Merger

def run(filepath):
    tmx_file = TMX_Merger(filepath)
    tmx_file.replace_newlines()
    tmx_file.create("replaced_save.tmx", is_print = False)

# Запуск програми
if __name__ == "__main__":
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    run("project_save.tmx")
