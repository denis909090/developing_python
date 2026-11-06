# 1.1
import math
def task_1_1_math_expressions():
    first_number = float(input("Введіть a - "))
    second_number = float(input("Введіть b- "))
    third_number = float(input("Введіть c - "))

    sum_of_squares = first_number ** 2 + second_number ** 2 + third_number ** 2
    average = (first_number + second_number + third_number) / 3
    discriminant = second_number ** 2 - 4 * first_number * third_number
    hypotenuse = math.sqrt(first_number ** 2 + second_number ** 2)
    is_triangle = (
        (first_number + second_number > third_number)
        and (first_number + third_number > second_number)
        and (second_number + third_number > first_number)
    )

    if second_number != 0:
        integer_quotient = first_number // second_number
        remainder = first_number % second_number
    else:
        integer_quotient = None
        remainder = None
 
    print()
    print(f"Сума квадратів- {sum_of_squares:.2f}")
    print(f"Середнє арифметичне- {average:.2f}")
    print(f"Дискримінант- {discriminant:.2f}")
    print(f"Гіпотенуза- {hypotenuse:.2f}")
    print(f"Чи є a, b, c сторонами трикутника - {'Так' if is_triangle else 'Ні'}")
 
    if integer_quotient is not None:
        print(f"a // b = {integer_quotient:.2f}, a % b = {remainder:.2f}")
    else:
        print("b дорівнює 0, ділити на нуль не можна")
 
 
#1.2
 
def task_1_2_type_converter():
    raw_text = input("Введіть число: ")
    try:
        number_as_float = float(raw_text)
    except ValueError:
        print("Введене значення не є числом")
        return
 
    number_as_int = int(number_as_float)
    number_as_bool = bool(number_as_float)
    number_as_text = str(number_as_float)
 
    print()
    print(f"float: {number_as_float}, тип - {type(number_as_float)}")
    print(f"int:   {number_as_int}, тип- {type(number_as_int)}")
    print(f"bool:  {number_as_bool}, тип- {type(number_as_bool)}")
    print(f"str:   '{number_as_text}', тип - {type(number_as_text)}")
    print(f"Чи є float числом - {isinstance(number_as_float, float)}")
    print(f"Довжина рядка числа -  {len(number_as_text)}")
 
    user_name = input("\nВведіть ім'я - ")
 
    try:
        user_age = int(input("Введіть вік - "))
    except ValueError:
        print("Вік має бути цілим числом")
        return
 
    print(f"Ім'я -  {user_name:<15}")
    print(f"Ім'я - {user_name:^15}")
    print(f"Ім'я-  {user_name:>15}")
    print(f"Вік з нулями - {user_age:03d}")
    print(f"Число з 3 знаками після коми і нулями - {number_as_float:08.3f}")

    numbers_range = range(1, 11, 2)
    numbers_list = list(numbers_range)
 
    print(f"\nСписок з range - {numbers_list}")
    print(f"Довжина списку -{len(numbers_list)}")
    print(f"id списк -{id(numbers_list)}")


task_1_1_math_expressions()

# Зчитуємо три числа і рахуємо суму квадратів, середнє, дискримінант,
# гіпотенузу, перевіряємо нерівність трикутника та ділення з залишком.  