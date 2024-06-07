#!/bin/bash

# ------------- Не вимагають знаходження у репозиторії ----------

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
	# if [ -n "$(git status --porcelain "$file_path" 2>/dev/null) " ]; then
	local uncommitted_files=$(git status --porcelain "$file_path" | awk '{print $2}') 
	# awk '{print $2}' отримує друге поле (слово) з кожного рядка вводу
    if [ -n "$uncommitted_files" ]; then
        echo "  Знайдено незакомічені зміни в $(basename "$file_path"):"
        echo "$uncommitted_files" | while read -r line; do echo "  + $(basename "$line")"; done
		# uncommitted_files=$(while read -r line; do echo "  $(basename "$line")"; done <<< "$uncommitted_files")
		# echo "$uncommitted_files"
        return 0
    else
		# echo "- Незакомічених змін не знайдено"
        return 1
    fi
}

# ------------- Вимагають знаходження у репозиторії -------------

# Функція для перевірки наявності незакомічених змін
check_uncommitted_changes() {
	local file_path="$1"
	if [ -n "$file_path" ]; then
		local status="$(git status --porcelain "$file_path" 2>/dev/null)"
	else
		local status="$(git status --porcelain)"
	fi
	
	# return "$status"
    if [ -n "$status" ]; then
        return 0  # є незакомічені зміни
    else
        return 1  # немає незакомічених змін
    fi
}

# Функція для перевірки наявності незакомічених змін
# check_uncommitted_changes() {
    # if [[ $(git status --porcelain) ]]; then
        # return 0  # є незакомічені зміни
    # else
        # return 1  # немає незакомічених змін
    # fi
# }

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
    
	if ! git remote | grep -q "^$remote_name$"; then
		echo "  Репозиторію $remote_name НЕ існує"
		return 1
	fi
	
    if git ls-remote --quiet --exit-code "$remote_name" "refs/heads/$branch_name" >/dev/null; then
        return 0  # гілка існує у віддаленому репозиторії
    else
        return 1  # гілка не існує у віддаленому репозиторії
    fi
}
# > /dev/null перенаправляє стандартний вивід(stdout) команди git ls-remote до спеціального файлу /dev/null, який фактично є "чорною дірою" для даних. При цьому код виходу (exit code) команди git ls-remote не буде змінений від цього перенаправлення виводу.

# Перевіряє, чи вказана тека є репозиторієм
is_git() {
	local dir="$1"
	
	if [ ! -d "$dir" ]; then
		echo "  $(basename "$dir") не існує"
		return 1
	fi
	
	if [ -d "$dir/.git" ] || git -C "$dir" rev-parse --is-inside-work-tree &>/dev/null; then
		# echo "  $(basename "$dir") є git репозиторієм"
		return 0
	else
		# echo "  $(basename "$dir") НЕ є git репозиторієм"
		return 1
	fi
}

# Видаляє суфікс _DialogeOmegaT_pl
remove_suffix() {
    local input_string="$1"
    local suffix="_DialogeOmegaT_pl"
    local length=${#suffix}
    
    # Перевірка, чи рядок закінчується суфіксом "_DialogeOmegaT_pl"
    if [[ "$input_string" == *"$suffix" ]]; then
        # Обрізаємо суфікс з кінця рядка
        local result="${input_string:0:-length}"
        echo "$result"
    else
        # Якщо рядок не має суфікса, просто повертаємо вхідний рядок
        echo "$input_string"
    fi
}

garbage_collect() {
	local dir="$1"
	if is_git "$dir" && ! check_uncommitted_changes "$dir"; then
		echo "  Очищення теки .git"
		cd "$dir"
		if git gc --aggressive --prune=all 2>/dev/null; then
			echo "  Теку .git успішно очищено"
		fi
	fi
}

# --------------------------------------------------------------

# Основна частина скрипту
# Можна використовувати для виконання команд у кожному репозиторії
main() {
	# echo "Функція main з git_functions.sh"
	local directory="$(get_directory)"
	local commits_number="$1"
	
    # local original_directory="$(pwd)"  # зберігаємо поточну теку

    # Перемикаємось до кожної підтеки заданої теки
    for dir in "$directory"/*/; do
        normalized_dir="$(realpath "$dir")"  # нормалізуємо шлях до директорії
        cd "$normalized_dir" || exit  # перемикаємося до нормалізованої директорії
        echo "Перевірка статусу git репозиторію в $normalized_dir"
		
		# garbage_collect "$normalized_dir"
		# get_last_commit_date "$normalized_dir" "$commits_number"
		# git remote -v
		# git config advice.addIgnoredFile false
		git fetch
		git remote rm upstream
		git remote prune origin
		
        # cd "$original_directory"  # повертаємося до початкової теки
    done
}

# Перевіряє наявність директорії
check_directory() {
	local directory="$1"
	if [ -d "$directory" ]; then
		return 0
	else
		echo -e "\tДиректорія $directory не існує"
		return 1
	fi
}

# Перевіряє наявність файлу
check_file() {
	local filename="$1"
	
	if [ -f "$filename" ]; then
		return 0
	else
		echo -e "\tФайл $filename не існує"
		return 1
	fi
}
# -e перевіряє наявність шляху, незалежно від того, це файл чи директорія

# Задає теку з репозиторіями для усіх суміжних скриптів
get_directory() {
	local directory="/d/Dropbox/Archolos/OmegaT/"	# робоча
	# local directory="/d/Archolos_test/Test_repos/"	# тест

	if check_directory "$directory"; then
		echo "$directory"
	else
		exit 1
	fi
}

get_dirname() {
	local dir_path="$1"
	# dir_path="/d/Archolos_test/Test_repos/Gliban/DialogeOmegaT/omegat/project_save.tmx"

	if [ -f "$file_path" ]; then
		dir_path="$(dirname "$dir_path")"
	# elif [ -d "$file_path" ]; then
		# dir_path="$file_path"
	fi
	
	echo "$dir_path"
	
	# echo "$dir_path"
	# git -C "$dir_path" add "$file_path"
}

# Перевірка, чи це основний виконуваний файл
# if __name__ == "__main__": # python
if [ "$0" == "$BASH_SOURCE" ]; then
	# echo "$(basename "$BASH_SOURCE") це основний виконуваний файл."
	main "$1"
	

# else
	# echo "Файл $BASH_SOURCE є включеним або імпортованим."
fi
