# Приклад словника з множинами
my_dict = {
    'set1': {1, 2, 3},
    'set2': {3, 4, 5},
    'set3': {5, 6, 7}
}

# Створюємо словник для зберігання унікальних значень
unique_values = {}

# Для кожного set у словнику
for key, value_set in my_dict.items():
    # Створюємо порожню множину для об'єднання всіх інших множин
    other_sets = set()

    # Додаємо всі інші множини, окрім поточної
    for k, v in my_dict.items():
        if k != key:  # Пропускаємо поточну множину
            other_sets.update(v)  # Додаємо значення до загальної множини

    # Унікальні значення — це ті, що є тільки в поточному set і не в інших
    unique_values[key] = value_set - other_sets

# Виводимо результат
for key, unique_set in unique_values.items():
    print(f"Унікальні значення для {key}: {unique_set}")
