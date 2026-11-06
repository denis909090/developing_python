import itertools
from collections import defaultdict, namedtuple
# 1.1
# Кожна функція використовує yield і віддає значення по одному, без списку в пам'яті
 
def arithmetic_progression(start: float, step: float):
    value = start
    while True:
        yield value
        value += step
 
 
def geometric_progression(start: float, ratio: float, limit: float = float("inf")):
    value = start
    while value <= limit:
        yield value
        value *= ratio

 
def fibonacci(n: int | None = None):
    previous, current = 0, 1
    count = 0
 
    while n is None or count < n:
        yield previous
        previous, current = current, previous + current
        count += 1
 
 
def collatz_sequence(n: int):
    current = n
    yield current
 
    while current != 1:
        if current % 2 == 0:
            current = current // 2
        else:
            current = 3 * current + 1
        yield current
 
 
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item
 
 
def task_2_1_generators():
    first_ap_values = list(itertools.islice(arithmetic_progression(2, 3), 10))
    print(f"Арифметична прогресія (2, 3): {first_ap_values}")
 
    gp_values = list(geometric_progression(1, 2, limit=1000))
    print(f"Геометрична прогресія (1, 2): {gp_values}")
 
    fib_15 = list(fibonacci(15))
    print(f"Фібоначчі (15): {fib_15}")
 
    coll_values = list(collatz_sequence(27))
    print(f"Коллатц (27): довжина={len(coll_values)}, макс={max(coll_values)}")
 
    nested = [1, [2, 3], [4, [5, 6]], 7, [8, [9, [10]]]]
    flat_values = list(flatten(nested))
    print(f"Розгортання: {flat_values}")
 
    for fib_number in fibonacci(None):
        if fib_number > 10000:
            print(f"Перше число Фібоначчі > 10000: {fib_number}")
            break
 
 
# 2.2
# Дані проходять через етапи по одному запису -> джерело - фільтр - парсинг - фільтр - вивід
 
SAMPLE_DATA = [
    "Олена,Математика,95",
    "Іван,Математика,78",
    "",
    "Марія,Фізика,92",
    "Петро,Математика,INVALID",
    "Анна,Фізика,88",
    "Олена,Фізика,90",
    "Іван,Програмування,85",
    "Марія,Програмування,91",
    "Петро,Фізика,76",
    "Анна,Математика,93",
    "Олена,Програмування,97",
    "",
    "Марія,Математика,89",
    "Іван,Фізика,72",
    "Петро,Програмування,80",
    "Анна,Програмування,86",
]
 
 
def data_source(records: list[str]):
    for record in records:
        yield record
 
 
def filter_empty(records):
    for record in records:
        if record.strip() != "":
            yield record
 
 
def parse_records(records):
    for record in records:
        parts = record.split(",")
 
        
        if len(parts) != 3:
            continue
 
        student_name, subject, grade_text = [part.strip() for part in parts]

        try:
            grade = int(grade_text)
        except ValueError:
            continue
 
        yield {"student": student_name, "subject": subject, "grade": grade}
 
 
def filter_passed(records, min_grade: int = 60):
    for record in records:
        if record["grade"] >= min_grade:
            yield record
 
 
def format_output(records):
    for record in records:
        yield f"[{record['subject']}] {record['student']}: {record['grade']} балів"
 
 
def task_2_2_pipeline():
    output_pipeline = format_output(
        filter_passed(
            parse_records(
                filter_empty(
                    data_source(SAMPLE_DATA)
                )
            ),
            min_grade=75,
        )
    )
 
    print("Результати")
    for line in output_pipeline:
        print(line)
 
    print("\nСередній бал по предметах")
    subject_grades = defaultdict(list)
 
    parsed_records = parse_records(filter_empty(data_source(SAMPLE_DATA)))
    for record in parsed_records:
        subject_grades[record["subject"]].append(record["grade"])
 
    for subject, grades in sorted(subject_grades.items()):
        average = sum(grades) / len(grades)
        print(f"  {subject}: {average:.1f} з {len(grades)} оцінок")


task_2_1_generators()
task_2_2_pipeline()