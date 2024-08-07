#!/bin/bash

source git_functions.sh

# Функція для додання незакомічених змін до індексу, створення коміту та відправки на сервер
commit_and_push_changes() {
	local file_path="$1"
    local commit_message="$2"
	
	# перевірка шляху
	if [ -z "$file_path" ]; then
        echo "  Не вказано шлях для додання незакомічених змін до індексу"
		return 1
	elif [ ! -e "$file_path" ]; then
		echo "  Шляху $file_path не існує"
		return 1
    fi
	# ------------------------------------------------------------------------
	# перевірка чи це файл, чи тека
	# якщо файл, то отримуємо батьківську теку
	if [ -f "$file_path" ]; then
		local dir_path="$(dirname "$file_path")"
	elif [ -d "$file_path" ]; then
		local dir_path="$file_path"
	fi
	# ------------------------------------------------------------------------
	# перевірка чи ця тека є частиною робочого дерева git
	# if ! is_git "$dir_path"; then
		# echo "  Шлях $dir_path не є репозиторієм"
		# return 1
	# fi
	# ------------------------------------------------------------------------
	# перевірка назви комміту
	if [ -z "$commit_message" ]; then
        commit_message="Автоматичний коміт $(date +'%d.%m.%Y %H:%M:%S')"
    fi
	# ------------------------------------------------------------------------
	# перевірка незакомічених змін
	if ! check_uncommitted_changes "$file_path"; then
		echo "  Немає незакомічених змін в $(basename "$file_path")"
		return 1
    fi
	# ------------------------------------------------------------------------
	# додання незакомічених змін до індексу
	if ! git -C "$dir_path" add "$file_path" 2> /dev/null; then
		echo "  При доданні $(basename "$file_path") до індексу сталася помилка"
		return 1
	fi
	# ------------------------------------------------------------------------
	# комміт
    if git -C "$dir_path" commit -m "$commit_message" --quiet; then
		echo "  Коміт \"$commit_message\" успішно створено"
	else
		echo "  При створенні коміту сталася помилка"
		return 1
	fi
	# ------------------------------------------------------------------------
	# відправка до віддаленого репозиторію
    if git -C "$dir_path" push --quiet 2> /dev/null; then
		echo "  Дані успішно відправлено до віддаленого репозиторію"
	else
		echo "  При відправці до віддаленого репозиторію сталася помилка"
		return 1
	fi
	# ------------------------------------------------------------------------
	return 0
}

# Основна частина скрипту
main() {
    local commit_message="$1"
	# local commit_message="Оновлені глосарії $(date +'%Y.%m.%d %H:%M:%S')"
    local root_directory="$(get_directory)"
    # local original_directory="$(pwd)"  # зберігаємо поточну теку для commit_and_push

    # Перемикаємось до кожної підтеки заданої теки
    for dir in "$root_directory"/*/; do
        normalized_dir=$(realpath "$dir")	# нормалізуємо шлях до директорії
        cd "$normalized_dir" || exit	# перемикаємося до нормалізованої директорії
        echo "Перевірка статусу git репозиторію в $(basename "$normalized_dir")"
		
		local project_save=$(realpath "$dir/DialogeOmegaT/omegat/project_save.tmx")
		local glossary=$(realpath "$dir/DialogeOmegaT/glossary/")	# тека з глосаріями
        
		if is_git "$normalized_dir"; then
			# помилки виводяться всередині
			# commit_and_push_changes "$glossary" "$commit_message"		# коммітимо глосарії
			commit_and_push_changes "$project_save" "$commit_message"	# коммітимо сейв
		else
			echo "  Шлях $normalized_dir не є репозиторієм"
			return 1
		fi
        
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

if [ "$0" == "$BASH_SOURCE" ]; then
	main "$1"   # $1 commit_message
fi
