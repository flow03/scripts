date_n_time="$(date +'%d.%m.%Y %H:%M:%S')"
# python_dir="../Python/lxml/"

./git_push.sh "Перед синхронізацією $date_n_time"
echo "------"
echo "Виконання python скрипта..."
python "../Python/lxml/TMX_merger.py" # "D:\Dropbox\Archolos\OmegaT"
echo "------"
./git_replace.sh "MERGED.tmx" # збережено в поточній теці
echo "------"
./git_push.sh "Синхронізація $date_n_time"
