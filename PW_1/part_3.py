#3.1 
def factorial(number: int) -> int:
    result = 1
    for current_number in range(2, number + 1):
        result = result * current_number
    return result
 
 
def harmonic_sum(number: int) -> float:
    total = 0.0
    for denominator in range(1, number + 1):
        total += 1 / denominator
    return total
 
 
def multiplication_table(number: int) -> None:
    for row in range(1, number + 1):
        row_text = ""
        for column in range(1, number + 1):
            row_text += f"{row * column:4d}"
        print(row_text)
 
 
def task_3_1_for_loops():
    number = int(input("Введіть число n: "))
 
    if number < 1:
        print("n має бути більше 0")
        return
 
    print(f"{number}! = {factorial(number)}")
    print(f"Гармонічна сума H({number}) = {harmonic_sum(number):.6f}")
 
    # range з параметрами start, stop, step: зворотний відлік з кроком -1
    countdown_text = ""
    for countdown_number in range(number, 0, -1):
        countdown_text += f"{countdown_number} "
    print(f"Зворотний відлік -{countdown_text}")
 
    # range з кроком 2: парні числа від 2 до n
    even_numbers = list(range(2, number + 1, 2))
    print(f"Парні числа до {number}: {even_numbers}")
 
    print(f"\nТаблиця множення {number}×{number}:")
    multiplication_table(number)
 
 
# 3.2
 
def task_3_2_calculator():
    print("Калькулятор")
    print("Введіть вираз - число оператор число")
    print("Введіть quit для виходу, history для історії")
 
    history = []
 
    while True:
        user_input = input("\n> ").strip()
        if user_input == "quit":
            break
        if user_input == "history":
            if len(history) == 0:
                print("Історія порожня")
            else:
                for record in history:
                    print(record)
            continue
        parts = user_input.split()
        if len(parts) != 3:
            print("формат має бути - число оператор число")
            continue
 
        first_text, operator, second_text = parts
 
        try:
            first_number = float(first_text)
            second_number = float(second_text)
        except ValueError:
            print("числа введено некоректно")
            continue
 
        # Перевірка ділення на нуль для /, // та %
        if operator in ("/", "//", "%") and second_number == 0:
            print("ділення на нуль")
            continue
 
        if operator == "+":
            result = first_number + second_number
        elif operator == "-":
            result = first_number - second_number
        elif operator == "*":
            result = first_number * second_number
        elif operator == "/":
            result = first_number / second_number
        elif operator == "//":
            result = first_number // second_number
        elif operator == "%":
            result = first_number % second_number
        elif operator == "**":
            result = first_number ** second_number
        else:
            print("невідомий оператор")
            continue
 
        record_text = f"{first_number} {operator} {second_number} = {result}"
        history.append(record_text)
        print(f"Результат-{result}")
 

task_3_1_for_loops()
task_3_2_calculator()

# Рахуємо факторіал і суму гармонічного ряду в циклі for, виводимо таблицю множення
# через вкладені цикли, а також зворотний відлік і парні числа через range з кроком