#!/bin/bash

source git_functions.sh

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

# Основна частина скрипту
main() {
	local directory="$(get_directory)"
	local commits_number="$1"
	
    # Перемикаємось до кожної підтеки заданої теки
    for dir in "$directory"/*/; do
        normalized_dir="$(realpath "$dir")"  # нормалізуємо шлях до директорії
        cd "$normalized_dir" || exit
        echo "Перевірка статусу git репозиторію в $normalized_dir"
		
		get_last_commit_date "$normalized_dir" "$commits_number"
    done
}

# Перевірка, чи це основний виконуваний файл
if [ "$0" == "$BASH_SOURCE" ]; then
	main "$1"
fi
