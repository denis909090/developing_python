from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Callable


# 3.1

from abc import ABC, abstractmethod
from datetime import datetime
import json

class SingletonMeta(type):
    
    _instances: dict[type, object] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class LogFormatter(ABC):
    
    @abstractmethod
    def format(self, level: str, message: str, timestamp: datetime) -> str:
        pass


class PlainFormatter(LogFormatter):
    
    def format(self, level: str, message: str, timestamp: datetime) -> str:
        return f"[{level}] {timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {message}"


class JSONFormatter(LogFormatter):
    
    def format(self, level: str, message: str, timestamp: datetime) -> str:
        return json.dumps({
            "level": level,
            "time": timestamp.isoformat(),
            "message": message
        }, ensure_ascii=False)


class ColorFormatter(LogFormatter):
    
    COLORS = {
        "DEBUG": "\033[90m",
        "INFO": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
    }
    RESET = "\033[0m"

    def format(self, level: str, message: str, timestamp: datetime) -> str:
        color = self.COLORS.get(level, self.RESET)
        time_str = timestamp.strftime('%H:%M:%S')
        return f"{color}[{level}]{self.RESET} {time_str} -> {message}"


class FormatterFactory:
    
    _formatters: dict[str, type[LogFormatter]] = {
        "plain": PlainFormatter,
        "json": JSONFormatter,
        "color": ColorFormatter,
    }

    @classmethod
    def register(cls, name: str, formatter_cls: type[LogFormatter]):
        cls._formatters[name] = formatter_cls

    @classmethod
    def create(cls, name: str) -> LogFormatter:
        if name not in cls._formatters:
            raise ValueError(f"Невідомий форматер: {name}")
        return cls._formatters[name]()

    @classmethod
    def available(cls) -> list[str]:
        return list(cls._formatters.keys())


class Logger(metaclass=SingletonMeta):
    LEVELS = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}

    def __init__(self, formatter_name: str = "plain", min_level: str = "DEBUG"):
        self._formatter = FormatterFactory.create(formatter_name)
        self._min_level = min_level
        self._log_history: list[str] = []

    def set_formatter(self, name: str):
        self._formatter = FormatterFactory.create(name)

    def log(self, level: str, message: str):
        if self.LEVELS[level] >= self.LEVELS[self._min_level]:
            formatted_msg = self._formatter.format(level, message, datetime.now())
            self._log_history.append(formatted_msg)
            print(formatted_msg)

    def debug(self, msg: str): self.log("DEBUG", msg)
    def info(self, msg: str): self.log("INFO", msg)
    def warning(self, msg: str): self.log("WARNING", msg)
    def error(self, msg: str): self.log("ERROR", msg)

    def get_history(self) -> list[str]:
        return self._log_history[:]


def main():
    logger1 = Logger("plain", "DEBUG")
    logger2 = Logger("json", "INFO")
    
    print(f"один і той самий об'єкт - {logger1 is logger2}\n")

    logger1.info("Система запущена")
    logger1.warning("Мало пам'яті")
    logger1.error("Помилка з'єднання")

    print("\n форматер на JSON")
    logger1.set_formatter("json")
    logger1.debug("Діагностика JSON")

    print("форматер на кольоровий -")
    logger1.set_formatter("color")
    logger1.info("Кольорове повідомлення")

    print(f"\n lоступні форматери - {FormatterFactory.available()}")
    print(f"sсторія логів - {len(logger1.get_history())} записів")

if __name__ == "__main__":
    main()


#3.2
class EventEmitter:
    def __init__(self):
        self._listeners: dict[str, list[Callable]] = {}

    def on(self, event: str, callback: Callable):
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)

    def off(self, event: str, callback: Callable):
        if event in self._listeners and callback in self._listeners[event]:
            self._listeners[event].remove(callback)

    def emit(self, event: str, *args, **kwargs):
        for callback in self._listeners.get(event, []):
            callback(*args, **kwargs)


class SortStrategy(ABC):
    @abstractmethod
    def sort(self, tasks: list["Task"]) -> list["Task"]:
        pass

class SortByPriority(SortStrategy):
    def sort(self, tasks: list["Task"]) -> list["Task"]:
        return sorted(tasks, key=lambda t: t.priority)

class SortByDeadline(SortStrategy):
    def sort(self, tasks: list["Task"]) -> list["Task"]:
        return sorted(tasks, key=lambda t: t.deadline)

class SortByCreationDate(SortStrategy):
    def sort(self, tasks: list["Task"]) -> list["Task"]:
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)


@dataclass
class Task:
    title: str
    priority: int  
    deadline: datetime
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)


class TaskModel(EventEmitter):
    def __init__(self):
        super().__init__()
        self._tasks: list[Task] = []

    def add_task(self, title: str, priority: int, deadline: datetime):
        task = Task(title=title, priority=priority, deadline=deadline)
        self._tasks.append(task)
        self.emit("task_added", task)

    def complete_task(self, index: int):
        if 0 <= index < len(self._tasks):
            task = self._tasks[index]
            task.completed = True
            self.emit("task_completed", task)

    def remove_task(self, index: int):
        if 0 <= index < len(self._tasks):
            task = self._tasks.pop(index)
            self.emit("task_removed", task)

    def get_tasks(self, include_completed: bool = True) -> list[Task]:
        if not include_completed:
            return [t for t in self._tasks if not t.completed]
        return self._tasks[:]

    def get_statistics(self) -> dict:
        total = len(self._tasks)
        completed = sum(1 for t in self._tasks if t.completed)
        return {
            "Всього": total,
            "Виконано": completed,
            "Активних": total - completed
        }



class TaskView:
    def show_tasks(self, tasks: list[Task], title: str = "Завдання"):
        print(f"\n {title}")
        print(f"{'№':<3} | {'Назва':<25} | {'Пріоритет':<10} | {'Дедлайн':<20} | {'Статус'}")
        print("-" * 75)
        for i, task in enumerate(tasks):
            status = "виконано" if task.completed else "не виконано"
            dt_str = task.deadline.strftime("%Y-%m-%d %H:%M")
            print(f"{i:<3} | {task.title:<25} | {task.priority:<10} | {dt_str:<20} | {status}")
        print("-" * 75)

    def show_message(self, message: str):
        print(f"[ПОДІЯ] {message}")

    def show_statistics(self, stats: dict):
        print("\n--- Статистика ---")
        for key, val in stats.items():
            print(f"{key}: {val}")


class TaskController:
    def __init__(self, model: TaskModel, view: TaskView):
        self._model = model
        self._view = view
        self._sort_strategy: SortStrategy = SortByPriority()

        self._model.on("task_added", lambda t: self._view.show_message(f"Додано: {t.title}"))
        self._model.on("task_completed", lambda t: self._view.show_message(f"Виконано: {t.title}"))
        self._model.on("task_removed", lambda t: self._view.show_message(f"Видалено: {t.title}"))

    def set_sort_strategy(self, strategy: SortStrategy):
        self._sort_strategy = strategy
        self._view.show_message(f"Стратегію сортування змінено на {strategy.__class__.__name__}")

    def add_task(self, title: str, priority: int, deadline: datetime):
        self._model.add_task(title, priority, deadline)

    def complete_task(self, index: int):
        self._model.complete_task(index)

    def show_all(self):
        tasks = self._model.get_tasks()
        sorted_tasks = self._sort_strategy.sort(tasks)
        self._view.show_tasks(sorted_tasks)

    def show_active(self):
        tasks = self._model.get_tasks(include_completed=False)
        sorted_tasks = self._sort_strategy.sort(tasks)
        self._view.show_tasks(sorted_tasks, title="Активні завдання")

    def show_stats(self):
        self._view.show_statistics(self._model.get_statistics())


def main():
    model = TaskModel()
    view = TaskView()
    ctrl = TaskController(model, view)
    now = datetime.now()

    ctrl.add_task("Вивчити метакласи", 1, now + timedelta(days=1))
    ctrl.add_task("Написати звіт", 3, now + timedelta(days=3))
    ctrl.add_task("Реалізувати MVC", 2, now + timedelta(days=2))
    ctrl.add_task("Купити каву", 5, now + timedelta(hours=2))
    ctrl.show_all()
    ctrl.set_sort_strategy(SortByDeadline())
    ctrl.show_all()
    ctrl.complete_task(0)
    
    ctrl.show_active()

    ctrl.show_stats()


if __name__ == "__main__":
    main()


