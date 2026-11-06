import sys
import timeit

# 3.1
# List зберігає всі елементи в пам'яті, generator — тільки правило обчислення.
 
def memory_comparison():

    sizes = [1_000, 10_000, 100_000, 1_000_000]
 
    print("=" * 60)
    print(f"{'N':>12} | {'list (байт)':>14} | {'gen (байт)':>12} | {'Ratio':>8}")
    print("-" * 60)
 
    for n in sizes:
        data_list = [x ** 2 for x in range(n)]
        data_gen = (x ** 2 for x in range(n))
 
        list_size = sys.getsizeof(data_list)
        gen_size = sys.getsizeof(data_gen)
 
        print(f"{n:>12,} | {list_size:>14,} | {gen_size:>12,} | {list_size / gen_size:>7.0f}×")
 
    print("=" * 60)
 
 
def performance_comparison():
    n = 500_000
 
    time_list = timeit.timeit(
        lambda: sum([x ** 2 for x in range(n)]),
        number=5,
    )
 
    time_gen = timeit.timeit(
        lambda: sum(x ** 2 for x in range(n)),
        number=5,
    )
 
    print(f"\nsum() для {n:,} елементів")
    print(f"  list comprehension: {time_list:.4f} с")
    print(f"  generator expression: {time_gen:.4f} с")
    faster = "list" if time_list < time_gen else "generator"
    print(f"  Швидше -{faster}")
 
 
def practical_usage():
    words = [
        "Python", "ітератор", "генератор", "yield", "comprehension",
        "дані", "пам'ять", "ефективність", "конвеєр", "ліниві",
        "обчислення", "протокол", "об'єкт", "клас", "функція",
    ]

    longest_length = max(len(word) for word in words)
    longest_word = next(word for word in words if len(word) == longest_length)
    print(f"Найдовше слово: '{longest_word}' ({longest_length} символів)")

    all_nonempty = all(len(word) > 0 for word in words)
    print(f"Всі слова непорожні: {all_nonempty}")
    has_long_word = any(len(word) > 15 for word in words)
    print(f"Є слово > 15 символів: {has_long_word}")

    csv_line = ",".join(word for word in words)
    print(f"CSV: {csv_line}")
 
    total_length = sum(len(word) for word in words)
    print(f"Сума довжин: {total_length}")
 
 
    word_lengths = {word: len(word) for word in words}
    print(f"Довжини: {word_lengths}")
 
    numbers = range(1, 101)
    even_squares_sum = sum(x ** 2 for x in numbers if x % 2 == 0)
    print(f"\nСума квадратів парних від 1 до 100: {even_squares_sum}")
 
 
memory_comparison()
performance_comparison()
practical_usage()