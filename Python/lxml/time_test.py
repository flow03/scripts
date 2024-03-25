from datetime import datetime

def parse_date_time():
    date_string = "20240222T203038Z"

    # Розбираємо рядок за допомогою методу strptime()
    date_time = datetime.strptime(date_string, "%Y%m%dT%H%M%SZ")

    # Виводимо результат
    print("Current date and time:", date_time)
    print("Дата та час:", date_time)

def compare_date_time():
    date_string1 = "20240223T203138Z"
    date_string2 = "20240223T203039Z"

    # Перетворюємо рядки у об'єкти datetime
    date_time1 = datetime.strptime(date_string1, "%Y%m%dT%H%M%SZ")
    date_time2 = datetime.strptime(date_string2, "%Y%m%dT%H%M%SZ")

    # Порівнюємо дати
    if date_time1 < date_time2:
        print("Date 1 < Date 2")
    elif date_time1 == date_time2:
        print("Date 1 == Date 2")
    else:
        print("Date 1 > Date 2")

# compare_date_time()
parse_date_time()
