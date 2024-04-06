#!/bin/bash

# Функція для отримання дати і повідомлення останнього коміту в репозиторії
get_last_commit_date() {
    local repo_path="$1"
	local num="$2"
	if [ -z "$num" ]; then
        num=1	# один коміт
    fi
    # local last_commit_date=$(cd "$repo_path" && git log -$num --format="%cd" --date=short)
	cd "$repo_path" || return 1
	local last_commit_info=$(git log -$num --pretty=format:"  %cd %s" --date=short)
    echo "$last_commit_info"
}

# Функція для перевірки наявності незакомічених змін у вказаному файлі чи теці, і виводу їх на екран
check_uncommitted_changes_print() {
	local file_path="$1"
    # Перевірка статусу за допомогою git status
	# if [ -n "$(git status --porcelain "$file_path")" ]; then
	local uncommitted_files=$(git status --porcelain "$file_path" | awk '{print $2}')
    if [ -n "$uncommitted_files" ]; then
        echo "+ Знайдено незакомічені зміни в $(basename "$file_path"):"
        echo "$uncommitted_files" | while read -r line; do echo "  $(basename "$line")"; done
		# uncommitted_files=$(while read -r line; do echo "  $(basename "$line")"; done <<< "$uncommitted_files")
		# echo "$uncommitted_files"
        return 0
    else
        return 1
    fi
}

# Функція для перевірки наявності незакомічених змін
check_uncommitted_changes() {
    if [[ $(git status --porcelain) ]]; then
        return 0  # є незакомічені зміни
    else
        return 1  # немає незакомічених змін
    fi
}

# Основна частина скрипту
main() {
    local directory="$1"
    # local original_directory="$(pwd)"  # зберігаємо поточну теку

    # Перемикаємо до кожної підтеки заданої теки
    for dir in "$directory"/*/; do
        normalized_dir=$(realpath "$dir")  # нормалізуємо шлях до директорії
        cd "$normalized_dir" || exit  # перемикаємося до нормалізованої директорії
        echo "Перевірка статусу git репозиторію в $normalized_dir"
		
        local project_save=$(realpath "$dir/DialogeOmegaT/omegat/project_save.tmx")
		local glossary=$(realpath "$dir/DialogeOmegaT/glossary/")	# тека з глосаріями
		
		# check_uncommitted_changes_print "$project_save"
		# check_uncommitted_changes_print "$glossary"
		
		get_last_commit_date "$normalized_dir" 3
		echo
		
        # cd "$original_directory"  # повертаємося до початкової теки
    done
}

directory="/d/Dropbox/Archolos/OmegaT/"

if [ ! -e "$directory" ]; then
	echo "Шлях $directory не існує"
	exit 1
else
	main "$directory"
fi
