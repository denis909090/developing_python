import time
import random

sizes = [100, 1000, 10000]

print("кро 1. пошук неіснуючого елемента")
print(f"{'N':<10} | {'Список':<15} | {'Множина':<15} | {'Словник':<15}")
print("-" * 65)

search_list_times = []

for n in sizes:
    data_list = [i * 2 for i in range(n)]
    data_set = set(data_list)
    data_dict = {i * 2: True for i in range(n)}
    
    target = -1

    start = time.perf_counter()
    for _ in range(100):
        target in data_list
    end = time.perf_counter()
    time_list = ((end - start) / 100) * 1000
    search_list_times.append(time_list)

    start = time.perf_counter()
    for _ in range(100):
        target in data_set
    end = time.perf_counter()
    time_set = ((end - start) / 100) * 1000

    start = time.perf_counter()
    for _ in range(100):
        target in data_dict
    end = time.perf_counter()
    time_dict = ((end - start) / 100) * 1000

    print(f"{n:<10} | {time_list:<15.5f} | {time_set:<15.5f} | {time_dict:<15.5f}")

print("---")

print("крок 2. побудова унікальних елементів з дублікатів")
print(f"{'N':<10} | {'Через список (ms)':<20} | {'Через множину (ms)':<20}")
print("-" * 60)

for n in sizes:
    raw_data = [random.randint(1, n // 2) for _ in range(n)]

    start = time.perf_counter()
    unique_list = []
    for x in raw_data:
        if x not in unique_list:
            unique_list.append(x)
    end = time.perf_counter()
    time_build_list = (end - start) * 1000

    start = time.perf_counter()
    unique_set = set()
    for x in raw_data:
        unique_set.add(x)
    end = time.perf_counter()
    time_build_set = (end - start) * 1000

    print(f"{n:<10} | {time_build_list:<20.5f} | {time_build_set:<20.5f}")

print("---")

print("крок 3. псевдографіка зростання часу пошуку в списку в залежності від N")
for i in range(len(sizes)):
    n = sizes[i]
    t = search_list_times[i]
    stars = "*" * int(t * 150)
    print(f"N = {n:<5} | {stars} ({t:.5f} ms)")