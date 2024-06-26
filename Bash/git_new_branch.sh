#!/bin/bash

source git_functions.sh

# Створює нову гілку з вказаним ім'ям
create_branch() {
	local normalized_dir="$1"
	local branch_name="$(remove_suffix "$(basename "$normalized_dir")")"
	local commit_message="Коміт перед створенням нової гілки $branch_name"
	
	if ! is_git "$normalized_dir"; then
		echo "  $(basename "$dir") НЕ є git репозиторієм"
		return 1
	fi
	# ------------------------------------------------------------------------
	echo "Перевірка статусу git репозиторію в $normalized_dir"
	if check_uncommitted_changes; then
		echo "  Знайдено незакомічені зміни в $(basename "$normalized_dir")"
		git add .
		if git commit -m "$commit_message" --quiet; then
			echo "  Коміт $commit_message успішно створено"
		else
			echo "  При створенні коміту сталася помилка"
			return 1
		fi
	else
		echo "  Немає незакомічених змін в $normalized_dir"
	fi
	# ------------------------------------------------------------------------
	# echo "Створення локальної гілки $branch_name"
	if ! branch_exists_locally "$branch_name"; then
		if git checkout -b "$branch_name" --quiet; then
			echo "  Локальну гілку $branch_name успішно створено"
		else
			echo "  При створенні локальної гілки сталася помилка"
			return 1
		fi
	else
		echo "  Локальна гілка $branch_name вже існує"
	fi
	# ------------------------------------------------------------------------
	# echo "Створення віддаленої гілки $branch_name"
	if ! branch_exists_remotely "$branch_name" "origin"; then
		if git push -u origin "$branch_name" --quiet 2> /dev/null; then
			echo "  Віддалену гілку $branch_name успішно створено"
		else
			echo "  При створенні віддаленої гілки сталася помилка"
			return 1
		fi
	else
		echo "  Віддалена гілка $branch_name вже існує"
		if git push --quiet 2> /dev/null; then # 2> /dev/null перенаправляє вихідний потік помилок (stderr) в нікуди
			echo "  Дані успішно відправлено до віддаленого репозиторію"
		else
			echo "  При відправці до віддаленого репозиторію сталася помилка"
			return 1
		fi
	fi
}

# Основна частина скрипту
main() {
    local directory="$(get_directory)"	# Замість цього вказувати шлях до репозиторію і назву нової гілки
	
	for dir in "$directory"/*/; do	# Позбутись циклу
		normalized_dir="$(realpath "$dir")"
		cd "$normalized_dir" || exit
		
		create_branch "$normalized_dir"

	done
}

# Перевірка наявності аргументів
# if [ $# -ne 1 ]; then
    # echo "Потрібно передати назву нової гілки"
    # exit 1
# else
	# branch_name="$1"
# fi

# directory="/d/Dropbox/Archolos/OmegaT/$1_DialogeOmegaT_pl"

# if [ -z "$branch_name" ]; then
    # echo "Не задано ім'я нової гілки"
    # exit 1
# else
	# main "$branch_name"
# fi

if [ "$0" == "$BASH_SOURCE" ]; then
	# main
fi
