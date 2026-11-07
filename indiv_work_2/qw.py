import threading
from u import LoggingMeta, validate_book_data

class Author(metaclass=LoggingMeta):
    def __init__(self, name):
        self.name = name

class Book(metaclass=LoggingMeta):
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year
        self.is_available = True  

class Reader(metaclass=LoggingMeta):
    def __init__(self, name):
        self.name = name

class Library(metaclass=LoggingMeta):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.books = []
        return cls._instance

    @validate_book_data
    def add_book(self, book):
        self.books.append(book)
        print(f"lодано книгу - '{book.title}'")

    def borrow_book(self, title, reader):
        with self._lock:
            for book in self.books:
                if book.title == title:
                    if book.is_available:
                        book.is_available = False
                        print(f"читач {reader.name} успішно взяв книгу '{title}'")
                        return
                    else:
                        print(f"читач {reader.name} хоче '{title}' але вона вже зайнята")
                        return
            print(f"книгу '{title}' не знайдено в базі")