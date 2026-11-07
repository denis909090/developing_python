import threading
import time
from qw import Library, Book, Author, Reader
from ex import InvalidDataError

def simulate_reader_request(reader_name, book_title):
    lib = Library()
    reader = Reader(reader_name)
    lib.borrow_book(book_title, reader)

def main():
    print(" ініціалізація системи")
    lib = Library()

    frank = Author("Іван Франко")
    book1 = Book("Захар Беркут", frank, 1883)
    book2 = Book("Перехресні стежки", frank, 1900)
    
    bad_book = Book("", frank, 2023) 

    print("\n додавання книг")
    try:
        lib.add_book(book1)
        lib.add_book(book2)
        lib.add_book(bad_book)
    except InvalidDataError as e:
        print(f"обробка виключення - {e}")

    print("\n запуск мульти запитів")
    requests = [
        ("Олексій", "Захар Беркут"),
        ("Марія", "Перехресні стежки"),
        ("Іван", "Захар Беркут")  
    ]

    threads = []
    for r_name, b_title in requests:
        t = threading.Thread(target=simulate_reader_request, args=(r_name, b_title))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\n hоботу системи завершено")

if __name__ == "__main__":
    main()