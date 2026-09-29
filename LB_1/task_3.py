file = open("text.txt", "r", encoding="utf-8")
raw_text = file.read()
file.close()

clean_text = raw_text.lower()
punctuation = [",", ".", "!", "?", "-", "—", ":", ";", "(", ")", '"']
for mark in punctuation:
    clean_text = clean_text.replace(mark, " ")

words = clean_text.split()

word_counts = {}
for word in words:
    if word in word_counts:
        word_counts[word] += 1
    else:
        word_counts[word] = 1

sorted_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)
sorted_by_key = sorted(word_counts.items())
print(sorted_by_key)

threshold = 2
filtered_word_counts = {k: v for k, v in word_counts.items() if v >= threshold}

char_counts = {}
for char in clean_text:
    if char != " " and char != "\n":
        if char in char_counts:
            char_counts[char] += 1
        else:
            char_counts[char] = 1

sorted_chars = sorted(char_counts.items(), key=lambda item: item[1], reverse=True)

print("Крок 1. повна частота слів")
for word, count in sorted_words:
    print(f"{word:<15} : {count}")
print()

print(f"Крок 2. відфільтрований словник")
for word, count in filtered_word_counts.items():
    print(f"{word:<15} : {count}")
print()

print("Крок 3. перевірка безпечного отримання частоти для відсутнього ключа")
search_word = "програмування"
safe_count = word_counts.get(search_word, 0)
print(f"Слово '{search_word}' зустрічається {safe_count} разів")
print()

print("Крок 4. Альтернативний режим")
for char, count in sorted_chars[:10]:
    print(f"Символ '{char}' : {count}")

output_file = open("result.txt", "w", encoding="utf-8")
output_file.write("Слово - Частота\n")
output_file.write("-" * 20 + "\n")
for word, count in sorted_words:
    output_file.write(f"{word} : {count}\n")
output_file.close()