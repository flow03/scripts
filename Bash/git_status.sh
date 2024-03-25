#!/bin/bash

# Функція для перевірки наявності незакомічених змін у вказаному файлі чи теці
check_uncommitted_changes() {
	local file_path="$1"
    # Перевірка статусу за допомогою git status
	if [ -n "$(git status --porcelain "$file_path")" ]; then
		return 0
	else
		return 1
	fi
}

# Основна частина скрипту
main() {
    local directory="$1"
    # local original_directory="$(pwd)"  # зберігаємо поточну теку

    # Перемикаємо до кожної підтеки заданої теки
    for dir in "$directory"/*/; do
        normalized_dir=$(realpath "$dir")  # нормалізуємо шлях до директорії
        cd "$normalized_dir" || exit  # перемикаємося до нормалізованої директорії
        echo "Перевірка статусу git репозиторію в $normalized_dir"
		
        local project_save=$(realpath "$dir/DialogeOmegaT/omegat/project_save.tmx")
		local glossary=$(realpath "$dir/DialogeOmegaT/glossary/")
		
        if check_uncommitted_changes "$project_save"; then
            echo "+ Знайдено незакомічені зміни в project_save.tmx"
		fi
		
		if check_uncommitted_changes "$glossary"; then
            echo "+ Знайдено незакомічені зміни в glossary"
        fi
        # cd "$original_directory"  # повертаємося до початкової теки
    done
}

directory="/d/Dropbox/Archolos/OmegaT/"

if [ ! -e "$directory" ]; then
	echo "Шлях $directory не існує"
	exit 1
else
	main "$directory"
fi
