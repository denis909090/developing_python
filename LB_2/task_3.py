# Лабораторна №2, Завдання 3
# Предметна область: обсяг даних (дисковий простір, бекапи)
# Одиниці двійкові: 1 KB = 1024 байти

UNITS = {
    "B": 1,
    "KB": 1024,
    "MB": 1024 ** 2,
    "GB": 1024 ** 3,
    "TB": 1024 ** 4,
}


class DataSize:
    def __init__(self, value, unit="B"):
        if unit not in UNITS:
            raise ValueError(f"Невідома одиниця: {unit}")
        if value < 0:
            raise ValueError("Обсяг даних не може бути від'ємним")
        # всередині все зберігаємо в байтах
        self.bytes = int(value * UNITS[unit])

    def __str__(self):
        for unit in ["TB", "GB", "MB", "KB"]:
            if self.bytes >= UNITS[unit]:
                return f"{self.bytes / UNITS[unit]:.2f} {unit}"
        return f"{self.bytes} B"

    def __repr__(self):
        return f"DataSize({self.bytes}, 'B')"

    def __add__(self, other):
        if not isinstance(other, DataSize):
            return NotImplemented 
        return DataSize(self.bytes + other.bytes)

    def __sub__(self, other):
        if not isinstance(other, DataSize):
            return NotImplemented
        if other.bytes > self.bytes:
            raise ValueError(f"Не можна відняти більше від меншого: {self} - {other}")
        return DataSize(self.bytes - other.bytes)

    def __mul__(self, k):
        if not isinstance(k, (int, float)):
            return NotImplemented
        return DataSize(self.bytes * k)

    def __rmul__(self, k):
        return self.__mul__(k)
    def __eq__(self, other):
        if not isinstance(other, DataSize):
            return NotImplemented
        return self.bytes == other.bytes

    def __lt__(self, other):
        if not isinstance(other, DataSize):
            return NotImplemented
        return self.bytes < other.bytes
    def __len__(self):
        return self.bytes

    def __call__(self, unit="B"):
        if unit not in UNITS:
            raise ValueError(f"Невідома одиниця: {unit}")
        return self.bytes / UNITS[unit]


# Демонстрація

a = DataSize(120, "GB")
b = DataSize(1.5, "TB")

print("=== 1. __str__ та __repr__ ===")
print(a)
print(repr(a))
print([a, b])

print()
print("=== 2. Арифметика ===")
print("a + b =", a + b)
print("b - a =", b - a)
print("a * 3 =", a * 3)
print("2 * a =", 2 * a)
result = a + b
print("Тип результату:", type(result).__name__)
print("Новий об'єкт:", result is not a and result is not b)

try:
    print(a - b)
except ValueError as e:
    print("ValueError:", e)

try:
    print(a + 5)
except TypeError as e:
    print("TypeError:", e)

print()
print("=== 3. Порівняння ===")
print("a == DataSize(120, 'GB'):", a == DataSize(120, "GB"))
print("a == b:", a == b)
print("a < b:", a < b)
print("b > a:", b > a)
c = DataSize(512, "MB")
print("sorted:", [str(x) for x in sorted([b, a, c])])

print()
print("=== 4. len() та виклик об'єкта ===")
print("len(a) =", len(a))
print("a('GB') =", a("GB"))
print("b('GB') =", b("GB"))
print("a('TB') =", a("TB"))

print()
print("=== 5. Практична ситуація: сховище ===")
total = DataSize(2, "TB")
used = b
free = total - used
new_backup = DataSize(600, "GB")
print("Всього:", total, "| Зайнято:", used, "| Вільно:", free)
if free < new_backup:
    print("Бекап", new_backup, "не поміститься!")
else:
    print("Бекап", new_backup, "поміститься")