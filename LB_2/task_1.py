class Server:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.is_running = True

    def check_health(self):
        if self.is_running:
            return "OK - сервер відповідає"
        return "ПОМИЛКА - сервер не відповідає"

    def __str__(self):
        return f"[{self.__class__.__name__}] {self.name} ({self.ip})"


class WebServer(Server):
    def __init__(self, name, ip, port, requests_per_sec):
        super().__init__(name, ip)
        self.port = port
        self.requests_per_sec = requests_per_sec

    def check_health(self):
        if not self.is_running:
            return "ПОМИЛКА - веб-сервер лежить"
        if self.requests_per_sec > 1000:
            return f"УВАГА - перевантаження, {self.requests_per_sec} запитів/с "
        return f"OK - порт {self.port}, {self.requests_per_sec} запитів/с"


class DatabaseServer(Server):
    def __init__(self, name, ip, db_name, connections, max_connections):
        super().__init__(name, ip)
        self.db_name = db_name
        self.connections = connections
        self.max_connections = max_connections

    def get_load_percent(self):
        return self.connections / self.max_connections * 100

    def check_health(self):
        if not self.is_running:
            return "ПОМИЛКА - база даних недоступна"
        load = self.get_load_percent()
        if load >= 90:
            return f"база {self.db_name} майже заповнена підключеннями ({load:.0f}%)"
        return f"OK. база {self.db_name}, підключень {self.connections}/{self.max_connections}"


class BackupServer(Server):
    def __init__(self, name, ip, disk_total_gb, disk_used_gb):
        super().__init__(name, ip)
        self.disk_total_gb = disk_total_gb
        self.disk_used_gb = disk_used_gb

    def get_free_gb(self):
        return self.disk_total_gb - self.disk_used_gb

    def check_health(self):
        if not self.is_running:
            return "сервер бекапів вимкнений"
        used_percent = self.disk_used_gb / self.disk_total_gb * 100
        if used_percent >= 80:
            return f"диск заповнений на {used_percent:.0f}%, вільно {self.get_free_gb()} ГБ"
        return f"вільно {self.get_free_gb()} ГБ"


# демонастрація
web = WebServer("web-01", "10.0.0.10", 80, 1500)
db = DatabaseServer("db-01", "10.0.0.20", "shop_db", 45, 100)
backup = BackupServer("backup-01", "10.0.0.30", 1000, 850)
backup2 = BackupServer("backup-02", "10.0.0.31", 2000, 400)
simple = Server("test-01", "10.0.0.99")


db.is_running = False

servers = [web, db, backup, backup2, simple]

print("Поліморфний обхід: check_health()")
for s in servers:
    print(s)
    print("   ->", s.check_health())

print()
print("isinstance()")
print("web це Server?", isinstance(web, Server))
print("web це WebServer?", isinstance(web, WebServer))
print("web це DatabaseServer?", isinstance(web, DatabaseServer))
print("simple це WebServer?", isinstance(simple, WebServer))

print()
print("issubclass()")
print("WebServer підклас Server?", issubclass(WebServer, Server))
print("BackupServer підклас Server?", issubclass(BackupServer, Server))
print("Server підклас WebServer?", issubclass(Server, WebServer))
print("DatabaseServer підклас BackupServer?", issubclass(DatabaseServer, BackupServer))

print()
print("Підрахунок за типами")
web_count = 0
for s in servers:
    if isinstance(s, WebServer):
        web_count += 1
print("Веб-серверів у списку:", web_count)