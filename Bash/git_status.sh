#!/bin/bash

source git_functions.sh

# Основна частина скрипту
main() {
    local directory="$(get_directory)"
    # local original_directory="$(pwd)"  # зберігаємо поточну теку

    # Перемикаємось до кожної підтеки заданої теки
    for dir in "$directory"/*/; do
        normalized_dir=$(realpath "$dir")  # нормалізуємо шлях до директорії
        cd "$normalized_dir" || exit  # перемикаємося до нормалізованої директорії
        echo "Перевірка статусу git репозиторію в $(basename "$normalized_dir")"
		
		# git remote
		
        local project_save=$(realpath "$dir/DialogeOmegaT/omegat/project_save.tmx")
		local glossary=$(realpath "$dir/DialogeOmegaT/glossary/")	# тека з глосаріями
		
		check_uncommitted_changes_print "$project_save"
		check_uncommitted_changes_print "$glossary"
		
		# get_last_commit_date "$normalized_dir" 3
		# echo
		
        # cd "$original_directory"  # повертаємося до початкової теки
    done
}

main # виклик