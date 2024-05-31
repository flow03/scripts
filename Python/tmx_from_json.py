# import os
import sys
# import time
import io
# import json
from .tmx.TMX_Merger import TMX_Merger
from .json.jsonFile import jsonFile

# ----------------------------------------------------

# def run_repos(repositories_path):
#     if os.path.isdir(repositories_path):
#         merger = TMX_Merger()
#         merger.merge_repos(repositories_path)

def run():
    pl_json = jsonFile()
    pl_json.load_loc("pl")
    uk_json = jsonFile()
    uk_json.load_loc("uk")

    tmx_file = TMX_Merger("test_project_save.tmx")

    tmx_file.load_json(pl_json, uk_json)
    tmx_file.create("json_project_save.tmx")

# Запуск програми
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    run()
