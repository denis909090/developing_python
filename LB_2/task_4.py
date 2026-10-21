from abc import ABC, abstractmethod

class SystemLogger:
    """Компонент для логування подій."""

    def __init__(self, log_file="system.log"):
        self.log_file = log_file

    def write_log(self, level, message):

        print(f"[{self.log_file}] [{level.upper()}]: {message}")



class BaseServer(ABC):
    """Абстрактний клас сервера."""

    def __init__(self, hostname, ip_address, logger=None):
        self.hostname = hostname
        self.ip_address = ip_address

        self.logger = logger if logger else SystemLogger()


    @property
    @abstractmethod
    def server_type(self):
        pass


    @abstractmethod
    def start_service(self, service_name):
        pass


    @abstractmethod
    def stop_service(self, service_name):
        pass


    def get_info(self):
        return f"Сервер: {self.hostname} | IP: {self.ip_address} | Тип: {self.server_type}"



class WebServer(BaseServer):

    def __init__(self, hostname, ip_address, max_connections=1000):
        super().__init__(hostname, ip_address)
        self.max_connections = max_connections

    @property
    def server_type(self):
        return "Web Server (Nginx)"

    def start_service(self, service_name):
        msg = f"Запуск веб-служби '{service_name}' на {self.hostname}"

        self.logger.write_log("INFO", msg)

    def stop_service(self, service_name):
        msg = f"Зупинка веб-служби '{service_name}' на {self.hostname}"
        self.logger.write_log("WARN", msg)



class DatabaseServer(BaseServer):

    def __init__(self, hostname, ip_address, db_engine="PostgreSQL"):
        super().__init__(hostname, ip_address)
        self.db_engine = db_engine

    @property
    def server_type(self):
        return f"Database Server ({self.db_engine})"

    def start_service(self, service_name):
        msg = f"Запуск СУБД '{service_name}' ({self.db_engine}) на {self.hostname}"
        
        self.logger.write_log("INFO", msg)

    def stop_service(self, service_name):
        msg = f"Аварійна зупинка СУБД '{service_name}' на {self.hostname}"
        self.logger.write_log("CRITICAL", msg)



if __name__ == "__main__":
    print("=== 1. Спроба створити екземпляр абстрактного класу ===")
    try:
        abstract_server = BaseServer("abstract-node", "0.0.0.0")
    except TypeError as e:
        print(f"Помилка перехоплена успішно: {e}\n")

    print("=== 2. Створення конкретних об'єктів ===")
    web_node = WebServer("web-prod-01", "192.168.1.10")
    db_node = DatabaseServer("db-prod-01", "192.168.1.20", db_engine="PostgreSQL")

    print(web_node.get_info())
    print(db_node.get_info())
    print()

    print("=== 3. Поліморфний виклик методів та Композиція (Делегування) ===")
    servers = [web_node, db_node]

    for server in servers:
        server.start_service("main_daemon")
        server.stop_service("main_daemon")
        print("-" * 40)