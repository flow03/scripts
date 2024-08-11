import timeit
from jsonFile import jsonFile

def run_static():
    repo = "D:\\Dropbox\\Archolos\\CoM_localization_repository\\pl"
    key = 'NAME_Bloodfly'

    value = jsonFile.find_value(repo, key)
    # print(key, ':', value)

def run_static_new():
    repo = "D:\\Dropbox\\Archolos\\CoM_localization_repository\\pl"
    key = 'NAME_Bloodfly'

    value = jsonFile.find_value_new(repo, key)
    # print(key, ':', value)


def time_test(func):
    _setup = "from __main__ import jsonFile, repo, key"

    func_name = func.__name__   # дозволяє отримати назву функції у вигляді рядка
    # print(func_name)
    _func_str = func_name + "()"
    _setup_str = "from __main__ import " + func_name

    # якщо функція передається рядком, то обов'язково потрібно вказати параметр setup
    # timer = timeit.Timer("jsonFile.find_value(repo, key)", setup=_setup)
    timer = timeit.Timer(_func_str, setup=_setup_str) 
    # timer = timeit.Timer(func)

    # print(timer.timeit(10))
    # print(timer.repeat(5, 10))
    for time in timer.repeat(5, 10):
        print(time)

# if __name__ == "__main__":
#     repo = "D:\\Dropbox\\Archolos\\CoM_localization_repository\\pl"
#     key = 'NAME_Bloodfly'

def time_tests():
    # print(timeit.timeit("jsonFile.find_value(repo, key)", setup=_setup, number=10))
    # print("-----------")
    # print(timeit.timeit("jsonFile.find_value_new(repo, key)", setup=_setup, number=10))

    # print(timeit.timeit(run_static, number=10))
    # print("-----------")
    # print(timeit.timeit(run_static_new, number=10))

    time_test(run_static)
    print("-----------")
    time_test(run_static_new)

if __name__ == "__main__":
    time_tests()
