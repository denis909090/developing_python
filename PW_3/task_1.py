#1.1
from abc import abstractmethod
import hashlib

class PluginMeta(type):
    _registry: dict[str, type] = {}
    REQUIRED_ATTRS = ("name", "version")

    def __new__(mcs, cls_name: str, bases: tuple, namespace: dict):
        cls = super().__new__(mcs, cls_name, bases, namespace)
        
        if bases:
            for attr in mcs.REQUIRED_ATTRS:
                if attr not in namespace:
                    raise TypeError(f"Клас {cls_name} повинен мати атрибут '{attr}'")
            mcs._registry[namespace["name"]] = cls
            
        return cls

    @classmethod
    def get_registry(mcs) -> dict[str, type]:
        return mcs._registry.copy()

    @classmethod
    def create_plugin(mcs, plugin_name: str):
        if plugin_name not in mcs._registry:
            raise ValueError(f"gлагін {plugin_name} не знайдено")
        return mcs._registry[plugin_name]()


class BasePlugin(metaclass=PluginMeta):
    @abstractmethod
    def execute(self, data: str) -> str:
        pass

class UpperPlugin(BasePlugin):
    name = "upper"
    version = "1.0"
    
    def execute(self, data: str) -> str:
        return data.upper()

class ReversePlugin(BasePlugin):
    name = "reverse"
    version = "1.0"
    
    def execute(self, data: str) -> str:
        return data[::-1]

class CensorPlugin(BasePlugin):
    name = "censor"
    version = "1.1"
    
    def execute(self, data: str) -> str:
        bad_words = ["Світ", "погане"]
        for word in bad_words:
            data = data.replace(word, "***")
        return data


HashPlugin = type(
    "HashPlugin", 
    (BasePlugin,), 
    {
        "name": "hash", 
        "version": "2.0", 
        "execute": lambda self, data: hashlib.md5(data.encode()).hexdigest()
    }
)

def main():
    print("зареєстровані плагіни")
    for name, cls in PluginMeta.get_registry().items():
        print(f"  {name} (v{cls.version}): {cls.__name__}")

    test_data = "Привіт Світ"
    print(f"\n тестові дані '{test_data}'")
    for name in PluginMeta.get_registry():
        plugin = PluginMeta.create_plugin(name)
        print(f"  {name}: {plugin.execute(test_data)}")

    print("\n спроба створити невалідний плагін ")
    try:
        class BadPlugin(BasePlugin):
            name = "bad"
            def execute(self, data: str) -> str: return data
    except TypeError as e:
        print(f"  очікувана помилка{e}")

if __name__ == "__main__":
    main()


# 1.2
class ValidatedField:
    def __init__(self, expected_type: type, min_value=None, max_value=None):
        self.expected_type = expected_type
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"'{self.public_name}' має бути типу {self.expected_type.__name__} отримано {type(value).__name__}")
        
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"Значення '{self.public_name}' не може бути менше {self.min_value}")
            
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"Значення '{self.public_name}' не може бути більше {self.max_value}")
            
        setattr(obj, self.private_name, value)


class ConfigSection:
    """Базовий клас секції конфігурації з автоматичною реєстрацією."""
    _sections: dict[str, type] = {}

    def __init_subclass__(cls, section_name: str = "", **kwargs):
        super().__init_subclass__(**kwargs)
        if section_name:
            cls._sections[section_name] = cls

    @classmethod
    def get_section(cls, name: str):
        return cls._sections.get(name)

    @classmethod
    def list_sections(cls) -> list[str]:
        return list(cls._sections.keys())


class DatabaseConfig(ConfigSection, section_name="database"):
    host = ValidatedField(str)
    port = ValidatedField(int, min_value=1, max_value=65535)
    max_connections = ValidatedField(int, min_value=1, max_value=1000)
    
    def __init__(self, host: str, port: int, max_connections: int):
        self.host = host
        self.port = port
        self.max_connections = max_connections


class LoggingConfig(ConfigSection, section_name="logging"):
    level = ValidatedField(str)
    max_file_size_mb = ValidatedField(int, min_value=1, max_value=1024)
    
    def __init__(self, level: str, max_file_size_mb: int):
        self.level = level
        self.max_file_size_mb = max_file_size_mb


def main():
    print("Зареєстровані секції - ", ConfigSection.list_sections())
    
    print("\n створення правильної конфігурації БД")
    db = DatabaseConfig(host="localhost", port=5432, max_connections=100)
    print(f"  БД {db.host}:{db.port}  макс підключень - {db.max_connections}")
    
    print("\n спроба встановити невірний тип")
    try:
        bad_db_type = DatabaseConfig(host="localhost", port="8080", max_connections=10)
    except TypeError as e:
        print(f"  Очікувана помилка {e}")
        
    print("\n якощ отримаємо значення поза діапазоном")
    try:
        bad_db_val = DatabaseConfig(host="localhost", port=5432, max_connections=5000)
    except ValueError as e:
        print(f"  Очікувана помилка: {e}")

if __name__ == "__main__":
    main()