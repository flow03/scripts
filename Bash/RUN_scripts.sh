./git_push.sh "Коміт перед синхронізацією $(date +'%Y-%m-%d')"
python ../Python/lxml/Gliban_Aedan_tmx_merger.py "D:\Dropbox\Archolos\OmegaT"
./git_replace.sh
./git_push.sh "Синхронізація $(date +'%Y-%m-%d')"
