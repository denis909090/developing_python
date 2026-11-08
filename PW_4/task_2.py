# 2.1

import threading
import time
import random

class BankAccount:
    def __init__(self, balance: float = 0.0):
        self.balance = balance
        self.transaction_count = 0

    def deposit(self, amount: float) -> None:
        current = self.balance
        time.sleep(random.uniform(0.0001, 0.001))
        self.balance = current + amount
        self.transaction_count += 1

    def withdraw(self, amount: float) -> bool:
        current = self.balance
        time.sleep(random.uniform(0.0001, 0.001))
        if current >= amount:
            self.balance = current - amount
            self.transaction_count += 1
            return True
        return False

class SafeBankAccount:
    def __init__(self, balance: float = 0.0):
        self.balance = balance
        self.transaction_count = 0
        self._lock = threading.Lock()

    def deposit(self, amount: float) -> None:
        with self._lock:
            current = self.balance
            time.sleep(random.uniform(0.0001, 0.001))
            self.balance = current + amount
            self.transaction_count += 1

    def withdraw(self, amount: float) -> bool:
        with self._lock:
            current = self.balance
            time.sleep(random.uniform(0.0001, 0.001))
            if current >= amount:
                self.balance = current - amount
                self.transaction_count += 1
                return True
            return False

def run_transactions(account, num_deposits: int, deposit_amt: float, num_withdrawals: int, withdraw_amt: float):

    def deposit_task(count, amt):
        for _ in range(count): account.deposit(amt)
        
    def withdraw_task(count, amt):
        for _ in range(count): account.withdraw(amt)

    threads = []
    dep_per_thread = num_deposits 
    with_per_thread = num_withdrawals    
    
    for _ in range(5):
        threads.append(threading.Thread(target=deposit_task, args=(dep_per_thread, deposit_amt)))
    for _ in range(5):
        threads.append(threading.Thread(target=withdraw_task, args=(with_per_thread, withdraw_amt)))

    for t in threads: t.start()
    for t in threads: t.join()

def main():
    initial_balance = 1000.0
    num_deposits = 100
    deposit_amount = 50.0
    num_withdrawals = 100
    withdraw_amount = 50.0

    expected_balance = (
        initial_balance
        + num_deposits * deposit_amount
        - num_withdrawals * withdraw_amount
    )

    print("Тест без синхронізації")
    unsafe_account = BankAccount(initial_balance)
    run_transactions(unsafe_account, num_deposits, deposit_amount, num_withdrawals, withdraw_amount)
    print(f"Фактичний баланс: {unsafe_account.balance:.2f} транзакцій: {unsafe_account.transaction_count}")
    print(f"Збігається з очікуваним: {abs(unsafe_account.balance - expected_balance) < 0.01}")

    print("\nТест із синхронізацією")
    safe_account = SafeBankAccount(initial_balance)
    run_transactions(safe_account, num_deposits, deposit_amount, num_withdrawals, withdraw_amount)
    print(f"Фактичний баланс: {safe_account.balance:.2f} транзакцій: {safe_account.transaction_count}")
    print(f"Збігається з очікуваним: {abs(safe_account.balance - expected_balance) < 0.01}")

    print(f"\nОчікуваний баланс: {expected_balance:.2f}")

if __name__ == "__main__":
    main()

# 2.2
# practical_04_task_2_2.py

class ConnectionPool:

    def __init__(self, max_connections: int = 3):
        self._semaphore = threading.Semaphore(max_connections)
        self._lock = threading.Lock()
        self.max_connections = max_connections
        self.active_connections = 0
        self.total_served = 0
        self.peak_connections = 0

    def acquire_connection(self, client_name: str) -> None:
        print(f"[{client_name}] Запит на з'єднання")
        self._semaphore.acquire()
        
        with self._lock:
            self.active_connections += 1
            if self.active_connections > self.peak_connections:
                self.peak_connections = self.active_connections
        
        print(f"[{client_name}] Отримав з'єднання.")

    def release_connection(self, client_name: str) -> None:
        with self._lock:
            self.active_connections -= 1
            self.total_served += 1
            
        print(f"[{client_name}] Звільнив з'єднання.")
        self._semaphore.release()

    def get_stats(self) -> dict:
        return {
            "max": self.max_connections,
            "active": self.active_connections,
            "total_served": self.total_served,
            "peak": self.peak_connections,
        }

def client_task(pool: ConnectionPool, client_name: str, ready_event: threading.Event) -> None:
    ready_event.wait()

    pool.acquire_connection(client_name)
    try:
        work_time = random.uniform(0.5, 2.0)
        print(f"  [{client_name}] Працює {work_time:.1f} сек (активних: {pool.active_connections})")
        time.sleep(work_time)
    finally:
        pool.release_connection(client_name)

def main():
    pool = ConnectionPool(max_connections=3)
    ready_event = threading.Event()
    num_clients = 10

    threads = []
    for i in range(num_clients):
        t = threading.Thread(
            target=client_task,
            args=(pool, f"Client-{i:02d}", ready_event),
        )
        threads.append(t)
        t.start()

    time.sleep(0.5)
    print("Сервер готовий. Усі клієнти починають роботу\n")
    ready_event.set()

    for t in threads:
        t.join()

    stats = pool.get_stats()
    print(f"\n статистика пулу ")
    print(f"Макс. з'єднань: {stats['max']}")
    print(f"Обслуговано клієнтів: {stats['total_served']}")
    print(f"Пікове навантаження: {stats['peak']}")

if __name__ == "__main__":
    main()