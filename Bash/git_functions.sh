#!/bin/bash

# ------------- Не вимагають перебувати у репозиторії ----------

# Функція для отримання дати і повідомлення останнього коміту в репозиторії
get_last_commit_date() {
    local repo_path="$1"
	local num="$2"
	if [ -z "$num" ]; then
        num=1	# один коміт
    fi
    # local last_commit_date=$(cd "$repo_path" && git log -$num --format="%cd" --date=short)
	cd "$repo_path" || return 1
	local last_commit_info=$(git log -$num --pretty=format:"  %cd %s" --date=short)
    echo "$last_commit_info"
}

# Функція для перевірки наявності незакомічених змін у вказаному файлі чи теці, і виводу їх на екран
check_uncommitted_changes_print() {
	local file_path="$1"
    # Перевірка статусу за допомогою git status
	# if [ -n "$(git status --porcelain "$file_path")" ]; then
	local uncommitted_files=$(git status --porcelain "$file_path" | awk '{print $2}')
    if [ -n "$uncommitted_files" ]; then
        echo "+ Знайдено незакомічені зміни в $(basename "$file_path"):"
        echo "$uncommitted_files" | while read -r line; do echo "  $(basename "$line")"; done
		# uncommitted_files=$(while read -r line; do echo "  $(basename "$line")"; done <<< "$uncommitted_files")
		# echo "$uncommitted_files"
        return 0
    else
		# echo "- Незакомічених змін не знайдено"
        return 1
    fi
}

# ------------- Вимагають cd repository ------------------------

# Функція для перевірки наявності незакомічених змін
check_uncommitted_changes() {
    if [[ $(git status --porcelain) ]]; then
        return 0  # є незакомічені зміни
    else
        return 1  # немає незакомічених змін
    fi
}

# Функція для додання незакомічених змін до індексу, створення коміту та відправки на сервер
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
	# ------------------------------------------------------------------------
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
    # if git push --quiet 2> /dev/null; then
		# echo "Дані успішно відправлено до віддаленого репозиторію"
	# else
		# echo "При відправці до віддаленого репозиторію сталася помилка"
		# return 1
	# fi
	# ------------------------------------------------------------------------
	return 0
}

# --------------------------------------------------------------

# Основна частина скрипту
main() {
	# echo "Функція main з git_functions.sh"

	local directory="$(get_directory)"
	
    # local original_directory="$(pwd)"  # зберігаємо поточну теку

    # Перемикаємось до кожної підтеки заданої теки
    for dir in "$directory"/*/; do
        normalized_dir=$(realpath "$dir")  # нормалізуємо шлях до директорії
        cd "$normalized_dir" || exit  # перемикаємося до нормалізованої директорії
        echo "Перевірка статусу git репозиторію в $normalized_dir"
		
		# git config advice.addIgnoredFile false
		
        # cd "$original_directory"  # повертаємося до початкової теки
    done
}

# Перевіряє наявність шляху
check_directory() {
	local directory="$1"
	if [ ! -e "$directory" ]; then
		echo "Шлях $directory не існує"
		# exit 1
		return 1
	else
		# echo "Шлях $directory існує"
		return 0
	fi
}

# Задає теку з репозиторіями для усіх суміжних скриптів
get_directory() {
	# directory="/d/Dropbox/Archolos/OmegaT/"
	local directory="/d/Archolos_test/Test_repos/"	# тест

	if check_directory "$directory"; then
		echo "$directory"
	else
		exit 1
	fi
}

# Перевірка, чи це основний виконуваний файл
# if __name__ == "__main__": # python
if [ "$0" == "$BASH_SOURCE" ]; then
	echo "$(basename "$BASH_SOURCE") це основний виконуваний файл."
	
	if check_directory "$(get_directory)"; then
		main "$(get_directory)"
	fi
# else
	# echo "Файл $BASH_SOURCE є включеним або імпортованим."
fi
