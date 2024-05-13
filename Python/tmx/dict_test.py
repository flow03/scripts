from collections import OrderedDict
# import sys
# import io

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def print_dict(dict):
    # Ітерація по словнику з впорядкованими ключами
    for key in sorted(dict.keys()):
        print(key, dict[key])
    # for key, value in dict:
        # print(key, value)

def dict_test():
    my_dict = {}

    # Додавання елементів з унікальними ключами
    my_dict['b'] = 2
    my_dict['a'] = 1
    my_dict['c'] = 3
    my_dict['c'] = 4
    
    # print_dict(my_dict)

    return my_dict
    
def ordered_dict_test():
    # Створення словника з впорядкованими ключами
    ordered_dict = OrderedDict()

    # Додавання елементів з впорядкованими ключами
    ordered_dict['c'] = 3
    ordered_dict['b'] = 2
    ordered_dict['a'] = 1

    # Ітерація по словнику з впорядкованими ключами
    for key in ordered_dict:
        print(key, ordered_dict[key])

def function(dict): # передача аргумента по посиланню
    dict['a'] = "string"
    dict['new'] = "new_value"

dict = dict_test()
print("Before function")
print_dict(dict)
print()
function(dict)
print("After function")
print_dict(dict)
