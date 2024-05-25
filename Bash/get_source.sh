#!/bin/bash

source git_functions.sh

# Основна частина скрипту
main() {
    local root_directory="$(get_directory)"
	
    # Перемикаємось до кожної підтеки заданої теки
    for dir in "$root_directory"/*/; do
        local normalized_dir=$(realpath "$dir")  # нормалізуємо шлях до директорії
        cd "$normalized_dir" || exit  # перемикаємося до нормалізованої директорії
        
		if is_git "$normalized_dir"; then
		    echo "Перевірка статусу git репозиторію в $(basename "$normalized_dir")"
			# find_source "$normalized_dir"
			if find_source "$normalized_dir"; then
				echo -e "\t----------"
				print_stats "$normalized_dir"
				echo -e "\t----------"
			fi
		else
			echo "$(basename "$normalized_dir") не є репозиторієм"
			return 1
		fi
        
    done
}

print_stats() {
	local project_stats="$(realpath "$1/DialogeOmegaT/omegat/project_stats.txt")"
	
	local unique="$(grep_word "$project_stats" "Унікальних:" 2)"
	local left="$(grep_word "$project_stats" "Залишилося унікальних:" 3)"
	local translated=$((unique-left))	# оператор арифметики
	
	echo -e "\tУнікальних:\t$unique"
	echo -e "\tПерекладено:\t$translated"
	echo -e "\tЗалишилося:\t$left"
}

grep_word() {
	local file="$1"
	local string="$2"
	# local num="$3"
	local result=$(grep -m 1 "^$string" "$file" | awk -v num="$3" '{print $num + 0; exit}')	# number
	echo "$result"
	
	# awk '{print $2; exit}' виводить друге слово в рядку і завершує виконання після першого знаходження
	# опція -v передає значення локальної змінної у awk
	# {$num + 0} перетворює значення у чисельний тип засобами awk
}

list() {
	local directory="$1"
	for dir in "$directory"/*/; do
		if check_directory "$dir"; then
			echo -e "\t$(basename "$dir")"
		fi
	done	
}

# ls
list_source() {
	local source_dir="$(realpath "$1/DialogeOmegaT/source/")"
	for dir in $(ls -d "$source_dir"/*/ 2>/dev/null); do
		echo -e "\t$(basename "$dir")"
	done
}

# find
find_source() {
	local source_dir="$(realpath "$1/DialogeOmegaT/source/")"
	local subdirs="$(find "$source_dir" -mindepth 1 -maxdepth 1 -type d)"
	
	if [ -n "$subdirs" ]; then
		# Ітерація по списку шляхів
		echo -e "\t----------"
		for dir in $subdirs; do	# не варто перетворювати subdirs у рядок
			echo -e "\t$(basename "$dir")"
		done
		return 0
	else
		# echo -e "\tСписок каталогів порожній або не знайдено каталогів"
		return 1
	fi
}

# Запуск
if [ "$0" == "$BASH_SOURCE" ]; then
	main
fi
