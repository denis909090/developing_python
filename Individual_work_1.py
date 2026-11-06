# Консольна програма з математичними обчисленнями, геометричними фігурами,
# структурами даних, ітераторами та генераторами

import math
from collections import defaultdict


# Кортеж з доступними фігурами
SUPPORTED_SHAPES = ("коло", "прямокутник", "трикутник")

# назви розмірів для кожної фігури
SIZE_LABELS = {
    "коло": ("радіус",),
    "прямокутник": ("ширина", "висота"),
    "трикутник": ("сторона a", "сторона b", "сторона c"),
}

def read_int(prompt: str, min_value: int = None, max_value: int = None) -> int:
    #Просить ввести ціле число, доки введення не буде коректним
    while True:
        text = input(prompt).strip()
        try:
            number = int(text)
        except ValueError:
            print("потрібно ввести ціле число")
            continue

        if min_value is not None and number < min_value:
            print(f"число має бути не менше {min_value}")
            continue
        if max_value is not None and number > max_value:
            print(f"число має бути не більше {max_value}")
            continue

        return number


def read_positive_float(prompt: str) -> float:
    # додаткове додатне число 
    while True:
        try:
            value = float(input(prompt).replace(",", "."))
        except ValueError:
            print("потрібно ввести число")
            continue

        if value <= 0:
            print("число має бути більше 0")
            continue

        return value



# 1 Математичні обчислення 

def factorial(number: int) -> int:
    # Факторіал числа через цикл for
    result = 1
    for current in range(2, number + 1):
        result *= current
    return result


def is_prime(number: int) -> bool:
    # Перевіряє, чи є число простим
    if number < 2:
        return False
    for divisor in range(2, int(math.sqrt(number)) + 1):
        if number % divisor == 0:
            return False
    return True


def fibonacci_list(count: int) -> list:
    # Повертає список перших count чисел фібоначчі 
    numbers = []
    previous, current = 0, 1
    while len(numbers) < count:
        numbers.append(previous)
        previous, current = current, previous + current
    return numbers


def run_math_tasks():
    
    number = read_int("Введіть число для факторіала  ", 0, 20)
    print(f"{number}! = {factorial(number)}")

    limit = read_int("Знайти прості числа до ", 1)
    # List comprehension: список простих чисел від 1 до limit
    primes = [value for value in range(1, limit + 1) if is_prime(value)]
    print(f"Прості числа до {limit}: {primes}")

    count = read_int("Скільки чисел фібоначчі вивести- ", 1)
    print(f"Фібоначчі- {fibonacci_list(count)}")



#  Геометричні фігури 


def is_valid_triangle(side_a: float, side_b: float, side_c: float) -> bool:
    # Перевіряє нерівність трикутника
    return (
        (side_a + side_b > side_c)
        and (side_a + side_c > side_b)
        and (side_b + side_c > side_a)
    )


def create_figure():
    
    print(f"Доступні фігури - {', '.join(SUPPORTED_SHAPES)}")
    shape = input("Оберіть фігуру - ").strip().lower()

    if shape not in SUPPORTED_SHAPES:
        print("такої фігури немає")
        return None

    
    if shape == "коло":
        size = (read_positive_float("Радіус: "),)
    elif shape == "прямокутник":
        width = read_positive_float("Ширин - ")
        height = read_positive_float("Висота - ")
        size = (width, height)
    else:
        side_a = read_positive_float("Сторона a: ")
        side_b = read_positive_float("Сторона b: ")
        side_c = read_positive_float("Сторона c: ")
        if not is_valid_triangle(side_a, side_b, side_c):
            print("такі сторони не утворюють трикутник")
            return None
        size = (side_a, side_b, side_c)

    
    return {"type": shape, "size": size}


def figure_area(figure: dict) -> float:
    
    shape = figure["type"]
    size = figure["size"]

    if shape == "коло":
        radius = size[0]
        return math.pi * radius ** 2
    elif shape == "прямокутник":
        width, height = size
        return width * height
    else:
        side_a, side_b, side_c = size
        half_perimeter = (side_a + side_b + side_c) / 2
        return math.sqrt(
            half_perimeter
            * (half_perimeter - side_a)
            * (half_perimeter - side_b)
            * (half_perimeter - side_c)
        )


def figure_perimeter(figure: dict) -> float:
    
    shape = figure["type"]
    size = figure["size"]

    if shape == "коло":
        return 2 * math.pi * size[0]
    elif shape == "прямокутник":
        width, height = size
        return 2 * (width + height)
    else:
        return sum(size)


def describe_figure(figure: dict) -> str:
    
    labels = SIZE_LABELS[figure["type"]]
    parts = [f"{label}={value}" for label, value in zip(labels, figure["size"])]
    return f"{figure['type']} ({', '.join(parts)})"



# 3  ітератори та генератори


class FigureIterator:
    

    def __init__(self, figures: list):
        self._figures = figures
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self) -> dict:
        if self._index >= len(self._figures):
            raise StopIteration

        figure = self._figures[self._index]
        self._index += 1
        return figure


class FigureCollection:
    

    def __init__(self):
        self._figures = []

    def add(self, figure: dict) -> None:
        self._figures.append(figure)

    def __iter__(self):
    
        return FigureIterator(self._figures)

    def __len__(self) -> int:
        return len(self._figures)


def area_generator(figures):
    
    for figure in figures:
        yield figure["type"], round(figure_area(figure), 2)


def big_figures_generator(figures, min_area: float):
    
    for figure in figures:
        if figure_area(figure) > min_area:
            yield figure



# Меню програми


def show_menu():
    print("\nМЕНЮ ")
    print("1. Факторіал, прості числа, Фібоначчі")
    print("2. Додати геометричну фігуру")
    print("3. Показати всі фігури (ітератор)")
    print("4. Площі фігур (генератор)")
    print("5. Фігури з площею більше заданої (генератор)")
    print("6. Статистика по типах фігур (словник)")
    print("0. Вихід")


def main():
    figure_collection = FigureCollection()

    while True:
        show_menu()
        choice = input("Ваш вибір: ").strip()

        if choice == "1":
            run_math_tasks()

        elif choice == "2":
            new_figure = create_figure()
            if new_figure is not None:
                figure_collection.add(new_figure)
                print("Фігуру додано")

        elif choice == "3":
            if len(figure_collection) == 0:
                print("Фігур ще немає")
            for figure in figure_collection:
                print(f"  {describe_figure(figure)}, периметр={figure_perimeter(figure):.2f}")

        elif choice == "4":
            if len(figure_collection) == 0:
                print("Фігур ще немає")
            for figure_type, area in area_generator(figure_collection):
                print(f"  {figure_type}: площа {area}")

        elif choice == "5":
            min_area = read_positive_float("Мінімальна площа - ")
            found = list(big_figures_generator(figure_collection, min_area))
            if len(found) == 0:
                print("Таких фігур немає")
            for figure in found:
                print(f"  {describe_figure(figure)}")

        elif choice == "6":
            
            counts = defaultdict(int)
            total_areas = defaultdict(float)
            for figure in figure_collection:
                counts[figure["type"]] += 1
                total_areas[figure["type"]] += figure_area(figure)

            if len(counts) == 0:
                print("Фігур ще немає")
            for shape_name in SUPPORTED_SHAPES:
                if shape_name in counts:
                    print(f"  {shape_name}: {counts[shape_name]} шт., "
                          f"сумарна площа {total_areas[shape_name]:.2f}")

        elif choice == "0":
            print("Програму завершено")
            break

        else:
            print("оберіть пункт з меню")


if __name__ == "__main__":
    main()