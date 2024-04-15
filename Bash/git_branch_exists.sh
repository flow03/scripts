#!/bin/bash

source git_functions.sh

# Основна частина скрипту
main() {
	local directory="$(get_directory)"
    # local branch_name="$1"
	
    # local original_directory="$(pwd)"  # зберігаємо поточну теку

    # Перемикаємось до кожної підтеки заданої теки
    for dir in "$directory"/*/; do
        normalized_dir="$(realpath "$dir")"  # нормалізуємо шлях до директорії
        cd "$normalized_dir" || exit  # перемикаємося до нормалізованої директорії
        echo "Перевірка наявності гілки $(basename "$normalized_dir") в git репозиторії $normalized_dir"
		
		local branch_name="$(basename "$normalized_dir")"
		
		if branch_exists_locally "$branch_name"; then
			echo "  Гілка $branch_name існує у локальному репозиторії"
		else
			echo "  Гілки $branch_name НЕ існує у локальному репозиторії"
		fi
		
		if branch_exists_remotely "$branch_name" "origin"; then
			echo "  Гілка $branch_name існує у віддаленому репозиторії"
		else
			echo "  Гілки $branch_name НЕ існує у віддаленому репозиторії"
		fi
	done
}

# Перевірка наявності аргументів
# if [ $# -ne 1 ]; then
    # echo "Потрібно передати назву гілки як аргумент"
    # exit 1
# fi

if [ "$0" == "$BASH_SOURCE" ]; then
	main # виклик головної функції з переданими аргументами
fi
