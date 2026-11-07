# для всіх помилок
class LibraryError(Exception):
    pass

# помилка при неправильних даних
class InvalidDataError(LibraryError):
    pass