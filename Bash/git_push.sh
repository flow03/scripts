#!/bin/bash

source git_functions.sh


# Функція для додання незакомічених змін до індексу, створення коміту та відправки на сервер
commit_and_push_changes() {
	local file_path="$1"
    local commit_message="$2"
	
	if [ -z "$file_path" ]; then
        echo "  Не вказано шлях для додання незакомічених змін до індексу"
		return 1
	elif [ ! -e "$file_path" ]; then
		echo "  Шляху $file_path не існує"
		return 1
    fi
	# ------------------------------------------------------------------------
	if [ -z "$commit_message" ]; then
        commit_message="Автоматичний коміт: $(date +'%Y-%m-%d %H:%M:%S')"
    fi
	# ------------------------------------------------------------------------
	if ! check_uncommitted_changes "$file_path"; then
		echo "  Немає незакомічених змін в $(basename "$file_path")"
		return 1
    fi
	# ------------------------------------------------------------------------
	if ! git add "$file_path" 2> /dev/null; then
		echo "  При доданні $(basename "$file_path") до індексу сталася помилка"
		return 1
	fi
	# ------------------------------------------------------------------------
    if git commit -m "$commit_message" --quiet; then
		echo "  Коміт $commit_message успішно створено"
	else
		echo "  При створенні коміту сталася помилка"
		return 1
	fi
	# ------------------------------------------------------------------------
    # if git push --quiet 2> /dev/null; then
		# echo "  Дані успішно відправлено до віддаленого репозиторію"
	# else
		# echo "  При відправці до віддаленого репозиторію сталася помилка"
		# return 1
	# fi
	# ------------------------------------------------------------------------
	return 0
}

# Основна частина скрипту
main() {
    local commit_message="$1"
    local root_directory="$(get_directory)"
    # local original_directory="$(pwd)"  # зберігаємо поточну теку для commit_and_push

    # Перемикаємось до кожної підтеки заданої теки
    for dir in "$root_directory"/*/; do
        normalized_dir=$(realpath "$dir")  # нормалізуємо шлях до директорії
        cd "$normalized_dir" || exit  # перемикаємося до нормалізованої директорії
        echo "Перевірка статусу git репозиторію в $(basename "$normalized_dir")"
		
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
