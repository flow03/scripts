from collections import OrderedDict
# import sys
# import io

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def dict_test():
    my_dict = {}

    # Додавання елементів з унікальними ключами
    my_dict['b'] = 2
    my_dict['a'] = 1
    my_dict['c'] = 3
    my_dict['c'] = 4

    # Ітерація по словнику з впорядкованими ключами
    # for key in sorted_keys:
        # print(key, my_dict[key])
        
    for key in sorted(my_dict.keys()):
    # for key in my_dict.keys():
        print(key, my_dict[key])
    

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

dict_test()
# ordered_dict_test()