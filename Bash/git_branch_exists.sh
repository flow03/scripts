#!/bin/bash

# Функція для перевірки наявності гілки у локальному репозиторії
branch_exists_locally() {
    local branch_name="$1"
    
    if git show-ref --quiet --verify "refs/heads/$branch_name"; then
        return 0  # гілка існує у локальному репозиторії
    else
        return 1  # гілка не існує у локальному репозиторії
    fi
}

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

# Основна частина скрипту
main() {
    local branch_name="$1"
    
    if branch_exists_locally "$branch_name"; then
        echo "Гілка $branch_name існує у локальному репозиторії"
    else
        echo "Гілка $branch_name не існує у локальному репозиторії"
    fi
    
    if branch_exists_remotely "$branch_name" "origin"; then
        echo "Гілка $branch_name існує у віддаленому репозиторії"
    else
        echo "Гілка $branch_name не існує у віддаленому репозиторії"
    fi
}

# Перевірка наявності аргументів
if [ $# -ne 1 ]; then
    echo "Потрібно передати назву гілки як аргумент"
    exit 1
fi

# виклик головної функції з переданими аргументами
main "$1"
