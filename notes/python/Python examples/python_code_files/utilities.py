def min_number(list):

    min_num = list[0]
    for n in list:
        if n < min_num:
            min_num = n

    return f'Minimum number in the list is {min_num}'

def max_number(list):

    max_num = list[0]
    for n in list:
        if n > max_num:
            max_num = n
    return f'Maximum number in the list is {max_num}'

def find_occurances(list, target):

    counter = 0
    for n in list:
        if n == target:
            counter += 1

    return f'Number of {target} in the list = {counter}'

def even_odd_numbers(list):

    even_nums = []
    odd_nums = []
    for n in list:
        if n % 2 == 0:
            even_nums.append(n)
        elif n % 2 != 0:
            odd_nums.append(n)

    return f'Even numbers in the list = {even_nums} and Odd numbers in the list = {odd_nums}'

if __name__ == '__main__':

    numbers = [5,6,2,3,4,4]
    #
    # # Minimum number from the list
    min_number(numbers)
    #
    # # Maximum number from the list
    max_number(numbers)
    #
    # # Even and odd numbers from the list
    # even_odd_numbers(numbers)
    #
    # # Repeating 10 in the list
    # find_occurances(numbers, 4)
    #
    # # Repeating numbers in the list
    # seen = set()
    # repeating = []
    # for n in numbers:
    #     if n in seen and n not in repeating:
    #         repeating.append(n)
    #     seen.add(n)
    #
    # print(f'Repeating numbers in the list = {repeating}')

