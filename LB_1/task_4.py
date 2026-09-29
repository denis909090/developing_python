list1 = [101, 102, 103, 104, 105, 101, 103]
list2 = [104, 105, 106, 107, 108, 105]
list3 = [101, 102]

print("Початкові списки з дублікатами")
print("Список 1-", list1)
print("Список 2-", list2)
print("Список 3-", list3)
print("---")

set1 = set(list1)
set2 = set(list2)
set3 = set(list3)

print("Крок 1. отримання унікальних елементів")
print("Множина 1-", sorted(set1))
print("Множина 2-", sorted(set2))
print("Множина 3-", sorted(set3))
print("---")

union_set = set1 | set2
intersection_set = set1 & set2
sym_diff_set = set1 ^ set2

print("Крок 2. операції над множинами 1 та 2")
print("Об'єднання-", sorted(union_set))
print("Перетин -", sorted(intersection_set))
print("Симетрична різниця- ", sorted(sym_diff_set))
print("---")

is_sub1 = set3 <= set1
is_sub2 = set2 <= set1

print("Крок 3: Перевірка відношення підмножини")
print(f"Чи є Множина 3 підмножиною Множини 1?  {is_sub1}")
print(f"Чи є Множина 2 підмножиною Множини 1?  {is_sub2}")
print("---")

print("Крок 4. додаткове завдання")

group_roles = frozenset(["read", "write"])
access_levels = {
    group_roles: "Адміністратор розробки"
}


print("Словник із ключем-frozenset-", access_levels)
print("Доступ за frozenset-ключем-", access_levels[group_roles])