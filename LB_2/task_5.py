from abc import ABC, abstractmethod

class NotificationStrategy(ABC):

    @abstractmethod
    def send(self, message: str) -> None:
        pass



class EmailNotification(NotificationStrategy):

    def __init__(self, email_address: str):
        self.email_address = email_address

    def send(self, message: str) -> None:
        print(f"[EMAIL -> {self.email_address}]: {message}")



class TelegramNotification(NotificationStrategy):

    def __init__(self, chat_id: str):
        self.chat_id = chat_id

    def send(self, message: str) -> None:
        print(f"[TELEGRAM -> Chat {self.chat_id}]: {message}")



class AlertManager:

    def __init__(self, strategy: NotificationStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: NotificationStrategy):

        self.strategy = strategy

    def notify(self, alert_text: str):
        print("--- Спрацював тригер моніторингу ---")

        self.strategy.send(alert_text)



class SlackNotification(NotificationStrategy):

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(self, message: str) -> None:
        print(f"[SLACK -> Webhook {self.webhook_url}]: {message}")



if __name__ == "__main__":
    print("=== 1. Базова робота паттерну Стратегія ===")
    email_strat = EmailNotification("admin@datacenter.local")
    alert_system = AlertManager(email_strat)

    alert_system.notify("Перевантаження CPU: 98% на Server-01")

    
    telegram_strat = TelegramNotification("@devops_alerts")
    alert_system.set_strategy(telegram_strat)
    alert_system.notify("Критично мало місця на диску DB-Cluster (5%)")

    print("\n=== 2. Демонстрація розширюваності (новий Slack-канал) ===")
    
    slack_strat = SlackNotification("https://hooks.slack.com/services/XYZ")
    alert_system.set_strategy(slack_strat)
    alert_system.notify("Втрачено зв'язок з комутатором Switch-Core-02")