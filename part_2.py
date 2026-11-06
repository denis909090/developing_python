# 2.1
def classify_grade(score: int) -> str:
    if score >= 90:
        return "A"
    elif score >= 82:
        return "B"
    elif score >= 74:
        return "C"
    elif score >= 64:
        return "D"
    elif score >= 60:
        return "E"
    elif score >= 35:
        return "FX"
    else:
        return "F"
 
 
def task_2_1_grade():
    try:
        score = int(input("Введіть оцінку - "))
    except ValueError:
        print("Оцінка має бути цілим числом")
        return
 
    if score < 0 or score > 100:
        print("Оцінка має бути від 0 до 100")
        return
 
    grade = classify_grade(score)
    print(f"Оцінка {score} -> ЄКТС - {grade}")
 
    passed = grade not in ("FX", "F")
    print(f"{'Зараховано' if passed else 'Не зараховано'}")
 
 
# 2.2
 
def triangle_type(side_a: float, side_b: float, side_c: float) -> str:
    is_triangle = (
        (side_a + side_b > side_c)
        and (side_a + side_c > side_b)
        and (side_b + side_c > side_a)
    )
 
    if is_triangle:
        if side_a == side_b and side_b == side_c:
            return "рівносторонній"
        else:
            sorted_sides = sorted([side_a, side_b, side_c])
            short_side_1 = sorted_sides[0]
            short_side_2 = sorted_sides[1]
            longest_side = sorted_sides[2]
 
            is_right = abs(short_side_1 ** 2 + short_side_2 ** 2 - longest_side ** 2) < 1e-9
 
            if is_right:
                return "прямокутний"
            elif side_a == side_b or side_b == side_c or side_a == side_c:
                return "рівнобедрений"
            else:
                return "різносторонній"
    else:
        return "не є трикутником"
 
 
def triangle_area(side_a: float, side_b: float, side_c: float) -> float:
    half_perimeter = (side_a + side_b + side_c) / 2
    area = math.sqrt(
        half_perimeter
        * (half_perimeter - side_a)
        * (half_perimeter - side_b)
        * (half_perimeter - side_c)
    )
    return area
 
 
def task_2_2_triangle():
    side_a = float(input("Введіть сторону a: "))
    side_b = float(input("Введіть сторону b: "))
    side_c = float(input("Введіть сторону c: "))
 
    kind = triangle_type(side_a, side_b, side_c)
    print(f"Тип трикутника - {kind}")
 

    if kind != "не є трикутником":
        area = triangle_area(side_a, side_b, side_c)
        print(f"Площа -{area:.2f}")


task_2_1_grade()
task_2_2_triangle()

# Спочатку перевіряємо, чи сторони утворюють трикутник, потім через вкладені if
# визначаємо тип трикутника. Площу рахуємо за формулою Герона, тільки для справжнього трикутника.