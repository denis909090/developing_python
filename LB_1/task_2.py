def unpack_student(student_tuple):
    surname, group, grades = student_tuple
    return surname, group, grades

def calculate_overall_average(students_list):
    total_sum = 0
    total_count = 0
    for student in students_list:
        surname, group, grades = student
        for grade in grades:
            total_sum += grade
            total_count += 1
    if total_count == 0:
        return 0.0
    average = total_sum / total_count
    return round(average, 2)

def convert_tuples_to_dicts(students_list):
    result_list = []
    for student in students_list:
        surname, group, grades = student
        student_dict = {
            "прізвище": surname,
            "група": group,
            "оцінки": grades
        }
        result_list.append(student_dict)
    return result_list

students = [
    ("Іваненко", "КН12540", [90, 85, 100, 95]),
    ("Петренко", "БІКС12540", [75, 80, 68, 90]),
    ("Сидоренко", "КІ12540", [88, 92, 94, 91]),
    ("Ковальчук", "БІКСб12540", [60, 70, 65, 80])
]

print("Крок 1. Список студентів")
print(f"{'Прізвище':<15} {'Група':<10} {'Оцінки':<20}")
print("-" * 45)
for st in students:
    s_name, s_group, s_grades = unpack_student(st)
    print(f"{s_name: <15} {s_group: <10} {str(s_grades): <20}")
print("---")

overall_avg = calculate_overall_average(students)
print("Крок 2. Агреговане значення")
print("середній бал усіх студентів -", overall_avg, "балів")
print("---")

print("Крок 3. заборона зміни елемента кортежу")
try:
    first_student = students[0]
    first_student[0] = "Шевченко"
except TypeError as error:
    print("помилка TypeError", error)
    print("Кортеж є незмінним, отже змінювати його елементи за індексом заборонено")
print("---")

print("Крок 4. демонстрація мутабельного вкладеного об'єкта")
sample_student = ("Бондаренко", "КН11", [80, 85, 90])

print("замінюємо кортеж")
print("Кортеж:", sample_student)
print("ID кортежу:", id(sample_student))
print("ID списку оцінок:", id(sample_student[2]))

sample_student[2].append(100)

print("Після зміни вкладеного списку:")
print("Кортеж:", sample_student)
print("ID кортежу:", id(sample_student))
print("ID списку оцінок:", id(sample_student[2]))
print("---")

print("Крок 5. додаткове завдання")
dicts_list = convert_tuples_to_dicts(students)
print("Результат перетворення")
for item in dicts_list:
    print(item)
print("---")

