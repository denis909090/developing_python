from collections import defaultdict, namedtuple
  
# Клас сам є ітератором: __next__ віддає числа від start до stop-1 з кроком step
# Коли діапазон закінчився, він починається знову, і так repeats разів

 
class CyclicRange:

    def __init__(self, start: int, stop: int, step: int = 1, repeats: int = 1):
        self._start = start
        self._stop = stop
        self._step = step
        self._repeats = repeats
 
        
        self._current = start
        self._cycle = 0
 
    def __iter__(self):
        
        return self
 
    def __next__(self) -> int:
        if self._cycle >= self._repeats:
            raise StopIteration
 
        value = self._current
        self._current += self._step
 
        if self._current >= self._stop:
            self._current = self._start
            self._cycle += 1
 
        return value
 
 
def task_1_1_cyclic_range():
    """Демонстрація CyclicRange з for, list(), sum()."""
    print("CyclicRange(1, 4, repeats=3):")
    for number in CyclicRange(1, 4, repeats=3):
        print(number, end=" ")
    print()
 
    print("\nCyclicRange(0, 10, step=3, repeats=2):")
    for number in CyclicRange(0, 10, step=3, repeats=2):
        print(number, end=" ")
    print()
 
    result_list = list(CyclicRange(5, 8, repeats=2))
    print(f"\nЯк список - {result_list}")
 
    total = sum(CyclicRange(1, 5, repeats=2))
    print(f"Сума CyclicRange(1, 5, repeats=2) - {total}")
 
 
# 1.2
# Ітератор проходить один раз і зберігає позицію. Контейнер при кожному for створює НОВИЙ ітератор, 
# тому обходів може бути скільки завгодно.
 
Student = namedtuple("Student", ["name", "grade"])
 
 
class StudentGroupIterator:
    """Ітератор для обходу StudentGroup."""
 
    def __init__(self, students: list[Student]):
        self._students = students
        self._index = 0
 
    def __iter__(self):
        return self
 
    def __next__(self) -> Student:
        if self._index >= len(self._students):
            raise StopIteration
 
        student = self._students[self._index]
        self._index += 1
        return student
 
 
class StudentGroup:
    def __init__(self, group_name: str):
        self._group_name = group_name
        self._students: list[Student] = []
 
    def add_student(self, name: str, grade: int) -> None:
        """Додає студента до групи."""
        self._students.append(Student(name, grade))
 
    def __iter__(self):
        return StudentGroupIterator(self._students)
 
    def __len__(self) -> int:
        return len(self._students)
 
    def top_students(self, n: int = 3):
        sorted_students = sorted(self._students, key=lambda s: s.grade, reverse=True)
        return StudentGroupIterator(sorted_students[:n])
 
 
def task_1_2_student_group():
    group = StudentGroup("КІ-21")
    group.add_student("Олена", 95)
    group.add_student("Іван", 78)
    group.add_student("Марія", 92)
    group.add_student("Петро", 85)
    group.add_student("Анна", 88)
 
    print("Перший обхід - ")
    for student in group:
        print(f"  {student.name}: {student.grade}")
 
    print("\nДругий обхід - ")
    for student in group:
        print(f"  {student.name}: {student.grade}")
 
    # Вкладений цикл: кожен студент з кожним (кожен for має свій ітератор)
    print("\nВсі пари студентів -")
    for first_student in group:
        for second_student in group:
            if first_student.name < second_student.name:
                print(f"  {first_student.name} та {second_student.name}")
 
    print("\nТоп-3 студенти  -")
    for student in group.top_students(3):
        print(f"  {student.name}: {student.grade}")


task_1_1_cyclic_range()
task_1_2_student_group()