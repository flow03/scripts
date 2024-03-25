#!/bin/bash

# Функція для перевірки наявності незакомічених змін
check_uncommitted_changes() {
    if [[ $(git status --porcelain) ]]; then
        return 0  # є незакомічені зміни
    else
        return 1  # немає незакомічених змін
    fi
}

# Функція для перевірки наявності гілки у локальному репозиторії
branch_exists_locally() {
    local branch_name="$1"
    
    if git show-ref --quiet --verify "refs/heads/$branch_name"; then
        return 0  # гілка існує у локальному репозиторії
    else
        return 1  # гілка не існує у локальному репозиторії
    fi
}
# У багатьох мовах програмування, включаючи і Bash, 0 вважається "успішним" кодом виходу, а будь-яке інше значення (не 0) вважається "невдалим". Умова if в мові Bash (і багатьох інших мовах програмування) інтерпретує 0 як істинне значення, тобто "успіх", а будь-яке інше значення вважається хибою або неправдивим.

# Функція для перевірки наявності гілки у віддаленому репозиторії
branch_exists_remotely() {
    local branch_name="$1"
    local remote_name="$2"
    
    if git ls-remote --quiet --exit-code "$remote_name" "refs/heads/$branch_name" > /dev/null; then
        return 0  # гілка існує у віддаленому репозиторії
    else
        return 1  # гілка не існує у віддаленому репозиторії
    fi
}
# > /dev/null перенаправляє стандартний вивід(stdout) команди git ls-remote до спеціального файлу /dev/null, який фактично є "чорною дірою" для даних. При цьому код виходу (exit code) команди git ls-remote не буде змінений від цього перенаправлення виводу.

# Основна частина скрипту
main() {
    local directory="$1"
    local branch_name="$2"
    # local original_directory="$(pwd)"  # зберігаємо поточну теку
	local commit_message="Частина перекладу $branch_name і оновлені глосарії"

	normalized_dir=$(realpath "$directory")  # нормалізуємо шлях до директорії
	cd "$normalized_dir" || exit  # перемикаємося до нормалізованої директорії
	# ------------------------------------------------------------------------
	echo "Перевірка статусу git репозиторію в $normalized_dir"
	if check_uncommitted_changes; then
		echo "Знайдено незакомічені зміни в $normalized_dir"
		git add .
		if git commit -m "$commit_message" --quiet; then
			echo "Коміт $commit_message успішно створено"
		else
			echo "При створенні коміту сталася помилка"
			exit 1
		fi
	else
		echo "Немає незакомічених змін в $normalized_dir"
	fi
	# ------------------------------------------------------------------------
	# echo "Створення локальної гілки $branch_name"
	if ! branch_exists_locally "$branch_name"; then
		if git checkout -b "$branch_name" --quiet; then
			echo "Локальну гілку $branch_name успішно створено"
		else
			echo "При створенні локальної гілки сталася помилка"
			exit 1
		fi
	else
		echo "Локальна гілка $branch_name вже існує"
	fi
	# ------------------------------------------------------------------------
	# echo "Створення віддаленої гілки $branch_name"
	if ! branch_exists_remotely "$branch_name" "origin"; then
		if git push -u origin "$branch_name" --quiet 2> /dev/null; then
			echo "Віддалену гілку $branch_name успішно створено"
		else
			echo "При створенні віддаленої гілки сталася помилка"
			exit 1
		fi
	else
		echo "Віддалена гілка $branch_name вже існує"
	fi
	# 2> /dev/null перенаправляє вихідний потік помилок (stderr) в нікуди
	# cd "$original_directory"  # повертаємося до початкової теки
}

directory="/d/Dropbox/Archolos/OmegaT/$1_DialogeOmegaT_pl"
branch_name="$1"

# Перевірка наявності аргументів
if [ $# -ne 1 ]; then
    echo "Потрібно передати назву нової гілки"
    exit 1
fi

directory="/d/Dropbox/Archolos/OmegaT/$1_DialogeOmegaT_pl"
branch_name="$1"

# if [ $# -ne 2 ]; then
    # echo "Потрібно передати шлях до репозиторію і назву нової гілки"
    # exit 1
if [ ! -e "$directory" ]; then
	echo "Шлях $directory не існує"
	exit 1
elif [ -z "$branch_name" ]; then
    echo "Не задано ім'я нової гілки"
    exit 1
else
	# echo "Виклик головної функції з переданими аргументами"
	# echo -e "branch_name:\t$branch_name"
	# echo -e "directory:\t$directory"
	main "$directory" "$branch_name"  # $1 directory, $2 branch_name
fi
