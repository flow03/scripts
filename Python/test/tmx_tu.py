import tmx
from datetime import datetime

# Поточна дата і час в потрібному форматі
current_time = datetime.now().strftime("%Y%m%dT%H%M%SZ")

# Створення TMX файлу
tmx_file = tmx.TMX()

# Створення TU (Translation Unit)
tu = tmx.TU()

# Додавання першого TUV (Translation Unit Variant) для польської мови
tuv_pl = tmx.TUV(lang='pl', seg='Żądło rzecznego krwiopijcy')
tu.append(tuv_pl)

# Додавання другого TUV (Translation Unit Variant) для української мови з атрибутами
tuv_uk = tmx.TUV(
    lang='uk', 
    seg='Жало річкового шершня',
    changeid="OmegaT Aligner", 
    changedate=current_time, 
    creationid="OmegaT Aligner", 
    creationdate=current_time
)
tu.append(tuv_uk)

# Додавання TU до TMX файлу
tmx_file.append(tu)

# Збереження TMX файлу у XML форматі
with open("tu_output.tmx", "w", encoding="utf-8") as f:
    tmx_file.writexml(f, pretty=True)

print("TMX файл створено успішно.")
