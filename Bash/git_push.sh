#!/bin/bash

source git_functions.sh

# Основна частина скрипту
main() {
    local commit_message="$1"
    local root_directory="$(get_directory)"
    # local original_directory="$(pwd)"  # зберігаємо поточну теку для commit_and_push

    # Перемикаємось до кожної підтеки заданої теки
    for dir in "$root_directory"/*/; do
        normalized_dir=$(realpath "$dir")  # нормалізуємо шлях до директорії
        cd "$normalized_dir" || exit  # перемикаємося до нормалізованої директорії
        echo "+ Перевірка статусу git репозиторію в $(basename "$normalized_dir")"
		
		local project_save=$(realpath "$dir/DialogeOmegaT/omegat/project_save.tmx")
		# local glossary=$(realpath "$dir/DialogeOmegaT/glossary/")	# тека з глосаріями
        
		commit_and_push_changes "$project_save" "$commit_message" # помилки виводяться всередині
        
        # cd "$original_directory"  # повертаємося до початкової теки
    done
}

# Перевірка наявності аргументів
# if [ $# -lt 1 ]; then
    # echo "Потрібно передати шлях до теки як аргумент"
    # exit 1
# else
	# main "$1" "$2"  # $1 root_directory, $2 commit_message
# fi

main "$1"   # $1 commit_message
