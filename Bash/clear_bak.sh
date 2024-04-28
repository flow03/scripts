#!/bin/bash

source git_functions.sh

# Основна частина скрипту
main() {
	local directory="$(get_directory)"
	local bak_directory="$1"

    for dir in "$directory"/*/; do
        normalized_dir="$(realpath "$dir")"	# нормалізуємо шлях до директорії
        cd "$normalized_dir" || exit 1	# перемикаємося до нормалізованої директорії
        echo "Перевірка статусу git репозиторію $(basename "$normalized_dir")"
		
		if is_git "$normalized_dir"; then
			local path="$(realpath "$normalized_dir/DialogeOmegaT/omegat/")"
			local bak_path="$bak_directory/$(basename "$normalized_dir")"
			
			create_directory "$bak_path"
			
			move "$path" "$bak_path"	# переносимо файли
		else
			echo "  $(basename "$normalized_dir") не є репозиторієм"
		fi
		
        # cd "$original_directory"  # повертаємося до початкової теки
    done
}

create_directory() {
	local directory="$1"
	if [ ! -d "$directory" ]; then
		if [ -f "$directory" ]; then
			if rm "$directory"; then	# видаляємо файл
				echo "  Файл $(basename "$directory") видалено"
			fi
		fi
		if mkdir "$directory"; then		# створюємо теку
			echo "  Директорію $(basename "$directory") створено"
		fi
	fi
}

check_bak() {
	local path="$1"
	local ext="*.bak"
	local count=$(find "$path" -type f -name "$ext" -print0 | grep -zc .)

	if [ $count == 0 ]; then
		echo "  Не знайдено файлів з розширенням $ext"
		return 1
	else
		local file=$(get_file_str $count)
		echo "  Знайдено $count $file з розширенням $ext"
		return 0
	fi
}

get_file_str() {
	local count="$1"
	# local str="файлів"
	if [ $count == 1 ]; then
		echo "файл"
	elif [ $count == 2 ] || [ $count == 3 ] || [ $count == 4 ]; then
		echo "файли"
	else
		echo "файлів"
	fi
}

# Основна функція програми
move() {
	local path="$1"
	local bak_path="$2"
	local ext="*.bak"
	
	local count=$(find "$path" -type f -name "$ext" -print0 | grep -zc .)
	
	if [ $count == 0 ]; then
		echo "  Не знайдено файлів з розширенням $ext"
		return 1
	else
		find "$path" -type f -name "$ext" -exec mv {} "$bak_path" \;
		echo "  $count $(get_file_str $count) з розширенням $ext успішно перенесено"
		return 0
	fi
}


if [ "$0" == "$BASH_SOURCE" ]; then
	main "/d/W/Archolos_files/Back/bak" # bak_directory
fi
