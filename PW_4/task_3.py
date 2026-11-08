#3.1
from concurrent.futures import (
    ThreadPoolExecutor,
    ProcessPoolExecutor,
    as_completed,
)

import threading
import queue
import random
import time
import hashlib

def io_bound_task(url: str) -> dict:
    time.sleep(0.5)
    return {"url": url, "status": 200, "size": len(url) * 42}

def cpu_bound_task(n: int) -> dict:
    hasher = hashlib.sha256()
    for i in range(n):
        hasher.update(str(i).encode())
    return {"n": n, "hash": hasher.hexdigest()[:16]}

def risky_task(value: int) -> float:
    if value == 0:
        raise ZeroDivisionError("Ділення на нуль!")
    if value < 0:
        raise ValueError(f"Від'ємне значення: {value}")
    return 1000.0 / value

def benchmark_io_bound():
    urls = [f"https://api.example.com/data/{i}" for i in range(20)]

    start = time.perf_counter()
    [io_bound_task(url) for url in urls]
    seq_time = time.perf_counter() - start

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=5) as executor:
        list(executor.map(io_bound_task, urls))
    par_time = time.perf_counter() - start

    print(f"Послідовно I/O: {seq_time:.3f} сек")
    print(f"Паралельно I/O (ThreadPool): {par_time:.3f} сек")
    print(f"Прискорення: {seq_time / par_time:.2f}x")

def benchmark_cpu_bound():
    tasks = [500_000] * 8

    start = time.perf_counter()
    [cpu_bound_task(t) for t in tasks]
    seq_time = time.perf_counter() - start

    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as executor:
        list(executor.map(cpu_bound_task, tasks))
    par_time = time.perf_counter() - start

    print(f"Послідовно CPU: {seq_time:.3f} сек")
    print(f"Паралельно CPU (ProcessPool): {par_time:.3f} сек")
    print(f"Прискорення: {seq_time / par_time:.2f}x")

def handle_exceptions():
    values = [10, 5, 0, -3, 8, 2]

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(risky_task, v): v for v in values}
        
        for future in as_completed(futures):
            val = futures[future]
            try:
                result = future.result()
                print(f"Успіх для {val}: {result:.2f}")
            except ZeroDivisionError as e:
                print(f"Помилка для {val}: {e}")
            except ValueError as e:
                print(f"Помилка для {val}: {e}")
            except Exception as e:
                print(f"Невідома помилка для {val}: {e}")

def main():
    print("=" * 60)
    print("ThreadPoolExecutor")
    print("=" * 60)
    benchmark_io_bound()

    print(f"\n{'=' * 60}")
    print("ProcessPoolExecutor")
    print("=" * 60)
    benchmark_cpu_bound()

    print(f"\n{'=' * 60}")
    print("Обробка виключень у пулах")
    print("=" * 60)
    handle_exceptions()

if __name__ == "__main__":
    main()




# 3.2

class Task:
    def __init__(self, task_id: int, data: str, priority: int = 0):
        self.task_id = task_id
        self.data = data
        self.priority = priority
        self.created_at = time.time()

    def __repr__(self):
        return f"Task(id={self.task_id}, data='{self.data}')"

def producer(task_queue: queue.Queue, num_tasks: int, producer_id: int) -> None:
    for i in range(num_tasks):
        task = Task(
            task_id=producer_id * 100 + i,
            data=f"Дані від виробника {producer_id}, пакет {i}",
            priority=random.randint(1, 5),
        )
        task_queue.put(task)
        print(f"[Виробник-{producer_id}] Створено: {task}")
        time.sleep(random.uniform(0.1, 0.3))
    
    # Сигнал завершення додається у main після завершення роботи всіх виробників

def consumer(task_queue: queue.Queue, consumer_id: int, results: list, results_lock: threading.Lock) -> None:
    while True:
        try:
            task = task_queue.get(timeout=2)
        except queue.Empty:
            print(f"  [Споживач-{consumer_id}] Черга порожня, завершення")
            break

        if task is None:
            # Передаємо сигнал завершення наступному споживачу
            task_queue.put(None)
            task_queue.task_done()
            print(f"  [Споживач-{consumer_id}] Отримано сигнал завершення")
            break

        time.sleep(random.uniform(0.2, 0.5))
        
        with results_lock:
            results.append(task)
            
        print(f"  [Споживач-{consumer_id}] Оброблено: {task.task_id}")
        task_queue.task_done()

def producer_consumer_demo():
    task_queue = queue.Queue(maxsize=5)
    results = []
    results_lock = threading.Lock()
    num_producers = 2
    num_consumers = 3
    tasks_per_producer = 5

    producers = []
    for i in range(num_producers):
        p = threading.Thread(target=producer, args=(task_queue, tasks_per_producer, i+1))
        producers.append(p)
        p.start()

    consumers = []
    for i in range(num_consumers):
        c = threading.Thread(target=consumer, args=(task_queue, i+1, results, results_lock))
        consumers.append(c)
        c.start()

    for p in producers:
        p.join()
    task_queue.put(None)

    for c in consumers:
        c.join()

    print(f"\nЗагалом оброблено задач: {len(results)}")
    print(f"Очікувалось задач-  {num_producers * tasks_per_producer}")

def deadlock_demo():
    lock_a = threading.Lock()
    lock_b = threading.Lock()
    deadlock_detected = threading.Event()

    def worker_1():
        lock_a.acquire()
        print("Захопив Lock A")
        time.sleep(0.1)
        acquired = lock_b.acquire(timeout=2)
        if not acquired:
            print("не вдалося захопити Lock B!")
            deadlock_detected.set()
            lock_a.release()
            return
        print("Захопив Lock B")
        lock_b.release()
        lock_a.release()

    def worker_2():
        lock_b.acquire()
        print("Захопив Lock B")
        time.sleep(0.1)
        acquired = lock_a.acquire(timeout=2)
        if not acquired:
            print("не вдалося захопити Lock A!")
            deadlock_detected.set()
            lock_b.release()
            return
        print(" Захопив Lock A")
        lock_a.release()
        lock_b.release()

    def safe_worker_1():
        with lock_a:
            print(" Захопив Lock A")
            time.sleep(0.1)
            with lock_b:
                print(" Захопив Lock B")

    def safe_worker_2():
        with lock_a:
            print("Захопив Lock A")
            time.sleep(0.1)
            with lock_b:
                print("Захопив Lock B")


    print("Спроба з потенційним дедлоком ")
    t1 = threading.Thread(target=worker_1)
    t2 = threading.Thread(target=worker_2)
    t1.start(); t2.start()
    t1.join(); t2.join()

    if deadlock_detected.is_set():
        print(" Дедлок виявлено.  timeout для запобігання зависанню\n")
    else:
        print(" Дедлок не виник \n")

    # Безпечна версія 
    print("Безпечна версія  ")
    t3 = threading.Thread(target=safe_worker_1)
    t4 = threading.Thread(target=safe_worker_2)
    t3.start(); t4.start()
    t3.join(); t4.join()
    print(" Безпечні потоки успішно завершили роботу без дедлоків")

def main():
    print("=" * 60)
    print("Паттерн Producer-Consumer ")
    print("=" * 60)
    producer_consumer_demo()

    print(f"\n{'=' * 60}")
    print("Демонстрація дедлоку ")
    print("=" * 60)
    deadlock_demo()

if __name__ == "__main__":
    main()