import multiprocessing
import time
import os
import threading
import time

def download_simulation(file_name: str, size_mb: float) -> dict:
    thread_name = threading.current_thread().name
    print(f"{thread_name} Початок завантаження '{file_name}' ({size_mb} MB)")
    
    sleep_time = size_mb * 0.5 
    time.sleep(sleep_time)
    
    print(f"[{thread_name}] Завершено завантаження '{file_name}'")
    
    return {"file": file_name, "size": size_mb, "thread": thread_name}

class MonitorThread(threading.Thread):
    def __init__(self, interval: float = 1.0):
        super().__init__(name="Monitor", daemon=True)
        self.interval = interval
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            print(f"[Monitor] Активних потоків у системі: {threading.active_count()}")
            time.sleep(self.interval)

    def stop(self):
        self._stop_event.set()

def main():
    files = [
        ("data.csv", 2.5),
        ("report.pdf", 1.0),
        ("image.png", 0.5),
        ("archive.zip", 4.0),
        ("log.txt", 0.3),
    ]

    print("gослідовне завантаження")
    start_seq = time.perf_counter()
    for file, size in files:
        download_simulation(file, size)
    seq_time = time.perf_counter() - start_seq

    print("\n Паралельне завантаження")
    monitor = MonitorThread(interval=0.5)
    monitor.start()

    threads = []
    results = [] 
    
    def worker(file_name, size_mb):
        res = download_simulation(file_name, size_mb)
        results.append(res)

    for i, (file_name, size_mb) in enumerate(files):
        t = threading.Thread(target=worker, args=(file_name, size_mb), name=f"Worker-{i+1}")
        threads.append(t)

    start_par = time.perf_counter()

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    par_time = time.perf_counter() - start_par
    
    monitor.stop()

    print(f"\nУсі файли завантажено паралельно за {par_time:.2f} сек")
    print(f"Послідовний час: {seq_time:.2f} сек")
    print(f"gрискорення - {seq_time / par_time:.2f}x")

if __name__ == "__main__":
    main()




# 2.1

def is_prime(n: int) -> bool:
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

def sum_primes_in_range(start: int, end: int) -> tuple[int, int, int]:
    pid = os.getpid()
    total_sum = 0
    count = 0
    
    for n in range(start, end):
        if is_prime(n):
            total_sum += n
            count += 1
            
    return (total_sum, count, pid)

def main():
    total_range = 1_000_000
    num_workers = 4

    chunk_size = total_range // num_workers
    ranges = []
    for i in range(num_workers):
        start = i * chunk_size if i > 0 else 2
        end = (i + 1) * chunk_size if i < num_workers - 1 else total_range
        ranges.append((start, end))

    start_time = time.perf_counter()
    seq_result = sum_primes_in_range(2, total_range)
    seq_time = time.perf_counter() - start_time

    start_time = time.perf_counter()
    with multiprocessing.Pool(processes=num_workers) as pool:
        par_results = pool.starmap(sum_primes_in_range, ranges)
    par_time = time.perf_counter() - start_time

    total_par_sum = sum(res[0] for res in par_results)
    total_par_count = sum(res[1] for res in par_results)
    
    print("\n результати паралельного виконання")
    for start, end, (r_sum, r_count, pid) in zip([r[0] for r in ranges], [r[1] for r in ranges], par_results):
        print(f"Діапазон [{start}-{end}): Знайдено {r_count} чисел")

    print(f"\nСума збігається: {seq_result[0] == total_par_sum}")
    print(f"Кількість чисел: {total_par_count}")
    print(f"Послідовно: {seq_time:.3f} сек")
    print(f"Паралельно ({num_workers} процеси): {par_time:.3f} сек")
    print(f"Прискорення: {seq_time / par_time:.2f}x")

if __name__ == "__main__":
    main()

    