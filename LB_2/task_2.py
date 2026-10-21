# датчик температури в серверній стійці
class TemperatureSensor:
    # межі, у яких датчик може працювати
    MIN_TEMP = -20
    MAX_TEMP = 100

    def __init__(self, sensor_id, location, temperature):
        self._sensor_id = sensor_id      
        self._location = location        
        self.__temperature = 0           
        self.temperature = temperature   

    @property
    def temperature(self):
        # getter
        return self.__temperature

    @temperature.setter
    def temperature(self, value):
        
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"Температура має бути числом, а не {type(value).__name__}")
        
        if value != value:
            raise ValueError("Температура не є числом (NaN)")
        if value < self.MIN_TEMP or value > self.MAX_TEMP:
            raise ValueError(
                f"Температура {value} поза діапазоном датчика "
                f"({self.MIN_TEMP}..{self.MAX_TEMP} °C)"
            )
        self.__temperature = value

    @property
    def temperature_f(self):
        
        return self.__temperature * 9 / 5 + 32

    @property
    def status(self):
        
        t = self.__temperature
        if t < 18:
            return "УВАГА - занизька"
        elif t <= 27:
            return "НОРМА"
        elif t <= 35:
            return "УВАГА - висока"
        else:
            return "КРИТИЧНО"

    def __str__(self):
        return f"Датчик {self._sensor_id} ({self._location}): {self.__temperature} °C"


# Демонстрація 

print(" 1. Створення з коректними даними ")
sensor = TemperatureSensor("T-01", "Стійка A3, холодний коридор", 22.5)
print(sensor)

print()
print(" 2. Некоректні значення ")
try:
    sensor.temperature = "гаряче"
except TypeError as e:
    print("TypeError:", e)

try:
    sensor.temperature = True
except TypeError as e:
    print("TypeError:", e)

try:
    sensor.temperature = 500
except ValueError as e:
    print("ValueError:", e)

try:
    sensor.temperature = float("nan")
except ValueError as e:
    print("ValueError:", e)

print("Температура після невдалих спроб:", sensor.temperature)

print()
print(" 3. Обчислювані властивості ")
print("Зараз:", sensor.temperature, "°C /", sensor.temperature_f, "°F /", sensor.status)
sensor.temperature = 30
print("Зараз:", sensor.temperature, "°C /", sensor.temperature_f, "°F /", sensor.status)
sensor.temperature = 40
print("Зараз:", sensor.temperature, "°C /", sensor.temperature_f, "°F /", sensor.status)

print()
print(" 4. Прямий доступ до __ атрибута та name mangling ")
try:
    print(sensor.__temperature)
except AttributeError as e:
    print("AttributeError:", e)

print("Через mangled-ім'я:", sensor._TemperatureSensor__temperature)

print()
print("5. Захищений атрибут ")
print("sensor._location =", sensor._location)