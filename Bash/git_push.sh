#!/bin/bash

# Функція для перевірки наявності незакомічених змін
check_uncommitted_changes() {
	local file_path="$1"
    # Перевірка статусу за допомогою git status
	local uncommitted_files=$(git status --porcelain "$file_path" | awk '{print $2}')
    if [ -n "$uncommitted_files" ]; then
        echo "+ Знайдено незакомічені зміни в $(basename "$file_path"):"
        echo "$uncommitted_files" | while read -r line; do echo "  $(basename "$line")"; done
        return 0
    else
        return 1
    fi
}

# Функція для додавання незакомічених змін до індексу, створення коміту та відправки на сервер
commit_and_push_changes() {
	local file_path="$1"
    local commit_message="$2"
	
	if [ -z "$file_path" ]; then
        echo "Не вказано шлях для додання незакомічених змін до індексу"
		return 1
    fi
	if [ -z "$commit_message" ]; then
        commit_message="Автоматичний коміт: $(date +'%Y-%m-%d %H:%M:%S')"
    fi
	
    # git config advice.addIgnoredFile false
    # git add ./omegat/project_save.tmx
	# git add ./glossary/*.txt
	if ! git add "$file_path" --quiet; then
		echo "При доданні $(basename "$file_path") до індексу сталася помилка"
		return 1
	fi	
	# ------------------------------------------------------------------------
    if git commit -m "$commit_message" --quiet; then
		echo "Коміт $commit_message успішно створено"
	else
		echo "При створенні коміту сталася помилка"
		return 1
	fi
	# ------------------------------------------------------------------------
    if git push --quiet 2> /dev/null; then
		echo "Дані успішно відправлено до віддаленого репозиторію"
	else
		echo "При відправці до віддаленого репозиторію сталася помилка"
		return 1
		# exit 1
	fi
	# ------------------------------------------------------------------------
	return 0
}

# Основна частина скрипту
main() {
    local root_directory="$1"
    local commit_message="$2"
    local original_directory="$(pwd)"  # зберігаємо поточну теку

    # Перемикаємо до кожної підтеки заданої теки
    for dir in "$root_directory"/*/; do
        normalized_dir=$(realpath "$dir")  # нормалізуємо шлях до директорії
        cd "$normalized_dir" || exit  # перемикаємося до нормалізованої директорії
        echo "Перевірка статусу git репозиторію в $normalized_dir"
		
		local project_save=$(realpath "$dir/DialogeOmegaT/omegat/project_save.tmx")
		# local glossary=$(realpath "$dir/DialogeOmegaT/glossary/")	# тека з глосаріями
        
        if check_uncommitted_changes "$project_save"; then
			commit_and_push_changes "$project_save" "$commit_message" # помилки виводяться всередині
        else
            echo "Немає незакомічених змін в $normalized_dir"
        fi
        
        cd "$original_directory"  # повертаємося до початкової теки
    done
}

# Перевірка наявності аргументів
if [ $# -lt 1 ]; then
    echo "Потрібно передати шлях до теки як аргумент"
    exit 1
fi

# виклик головної функції з переданими аргументами
main "$1" "$2"  # $1 root_directory, $2 commit_message
