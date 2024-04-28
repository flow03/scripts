#!/bin/bash

source git_functions.sh

# Основна частина скрипту
main() {
    local root_directory="$(get_directory)" # з файлу git_functions.sh
	local file_path="$1"
    # local original_directory="$(pwd)"  # зберігаємо поточну теку для commit_and_push

    # Перемикаємось до кожної підтеки заданої теки
    for dir in "$root_directory"/*/; do
        normalized_dir="$(realpath "$dir")"	# нормалізуємо шлях до директорії
        cd "$normalized_dir" || exit 1	# перемикаємося до нормалізованої директорії
        # echo "Перевірка статусу git репозиторію в $(basename "$normalized_dir")"
		
		local project_save="$(realpath "$normalized_dir/DialogeOmegaT/omegat/project_save.tmx")"
		# local glossary=$(realpath "$normalized_dir/DialogeOmegaT/glossary/")	# тека з глосаріями
		
		if check_uncommitted_changes "$project_save"; then
			echo "Знайдено незакомічені зміни в $(basename "$normalized_dir"):"
			echo "Продовжити копіювання? (y/n)"
			read answer
			if [ "$answer" == "y" ] || [ "$answer" == "yes" ]; then
				copy "$file_path" "$project_save" "$normalized_dir"
			fi
		else
			copy "$file_path" "$project_save" "$normalized_dir"
        fi
		
        # cd "$original_directory"  # повертаємося до початкової теки
    done
}

copy() {
	local file_path="$1"
	# local repo="$2"
	# local project_save="$(realpath "$repo/DialogeOmegaT/omegat/project_save.tmx")"
	# repo="$(basename "$repo")"
	local project_save="$2"
	local repo="$(basename "$3")"
	
	if cp -f "$file_path" "$project_save"; then
		echo "Файл $(basename "$file_path") успішно скопійовано у $repo"
		# return 1
	else
		echo "При копіюванні $(basename "$file_path") у $repo сталася помилка"
	fi	
}

if [ "$0" == "$BASH_SOURCE" ]; then
	# Перевірка наявності аргументів
	if [ $# -lt 1 ]; then # -lt less than, -gt greater than
		filename="MERGED.tmx"
	else
		filename="$1"
	fi
	# Перевірка наявності файлу
	if check_file "$filename"; then
		file_path="$(realpath "$filename")"
		main "$file_path"
	fi
fi
