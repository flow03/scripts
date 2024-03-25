#!/bin/bash

# Функція для перевірки наявності незакомічених змін
check_uncommitted_changes() {
    if [[ $(git status --porcelain) ]]; then
        return 0  # є незакомічені зміни
    else
        return 1  # немає незакомічених змін
    fi
}

# Функція для додавання незакомічених змін до індексу, створення коміту та відправки на сервер
commit_and_push_changes() {
    local commit_message="$1"
	
    # git config advice.addIgnoredFile false
    git add ./omegat/project_save.tmx
	git add ./glossary/*.txt
    git commit -m "$commit_message"
    # git push # змініть "origin" і "master" на ваші дані
}

# Основна частина скрипту
main() {
    local directory="$1"
    local commit_message="$2"
    local original_directory="$(pwd)"  # зберігаємо поточну теку

    # Перемикаємо до кожної підтеки заданої теки
    for dir in "$directory"/*/; do
        normalized_dir=$(realpath "$dir")  # нормалізуємо шлях до директорії
        cd "$normalized_dir" || exit  # перемикаємося до нормалізованої директорії
        echo "Перевірка статусу git репозиторію в $normalized_dir"
        
        if check_uncommitted_changes; then
            echo "Знайдено незакомічені зміни в $normalized_dir"
            if [ -z "$commit_message" ]; then
                default_commit_message="Автоматичний коміт: $(date +'%Y-%m-%d %H:%M:%S')"
                commit_and_push_changes "$default_commit_message"
            else
                commit_and_push_changes "$commit_message"
            fi
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
main "$1" "$2"  # $1 directory, $2 commit_message
