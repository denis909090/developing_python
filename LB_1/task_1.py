file = open("num.txt", "r")
content = file.read()
file.close()

str_numbers = content.split()
numbers = []

for item in str_numbers:
    numbers.append(int(item))



print("---")
print("Початковий список з файлу:")
print(numbers)
print(id(numbers))
print("---")


pos_el = numbers[2]
neg_el = numbers[-2]

print("---")
print("Елемент за додатним індексом 2:", pos_el)
print("Елемент за від’ємним індексом -2:", neg_el)
print("---")

slice1 = numbers[1:6]
slice2 = numbers[::2]
slice3 = numbers[1:8:3]

print("---")
print("Зріз - від 1 до 6. індекси з 1 по 5 - ", slice1)
print("id зрізу 1 -",id(slice1))
print("Зріз - весь список. через один - ", slice2)
print("id зрізу 2- ",id(slice2))
print("Зріз - від 1 до 8. індекси з 1 по 7, крок 3 - ", slice3)
print("id зрізу 3 -",id(slice3))
print("---")
print(numbers)
print("---")

print("---")
numbers.append(100)
print("---")
print("1 мутація. додав 100 в кінець списку")
print("id списку numbers-", id(numbers))
print("Поточний список - ", numbers)

print("---")
numbers.insert(0, 999)
print("мутація 2. додав 999 на початок з нульовим індексом")
print(id(numbers))
print("Поточний список - ", numbers)



print("---")
numbers[3] = 555
print("3 мутація. замінив елемент за індексом 3 на 555")
print("Поточний список - ", numbers)
print(id(numbers))
print("---")

deleted_val = numbers.pop(-1)
print("---")
print("4 мутація. видалив останній елемент", deleted_val)
print(id(numbers))
print("Фінальний список:", numbers)
print("---")