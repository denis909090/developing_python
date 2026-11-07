from ex import InvalidDataError

# виводить повідомлення коли створюється новий клас у пам'яті
class LoggingMeta(type):
    def __new__(cls, name, bases, dct):
        print(f"створено новий клас у системі - {name}")
        return super().__new__(cls, name, bases, dct)


def validate_book_data(func):
    def wrapper(self, book, *args, **kwargs):
        if not book.title or not book.author:
            raise InvalidDataError("книга повинна мати назву та автора")
        return func(self, book, *args, **kwargs)
    return wrapper