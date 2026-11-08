import os
import sys

def setup_django_files():
    os.makedirs('mysite/pages', exist_ok=True)
    os.makedirs('mysite/mysite', exist_ok=True)
    
    with open('mysite/pages/views.py', 'w', encoding='utf-8') as f:
        f.write("""from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>Головна</h1><p>Опис проекту</p><ul><li>Пункт 1</li><li>Пункт 2</li><li>Пункт 3</li></ul>")

def about(request):
    return HttpResponse("Курс: Веб-розробка<br>ПР: 5<br>Студент: Ім'я Прізвище")

def contact(request):
    name = request.GET.get('name')
    if name:
        return HttpResponse(f"Привіт, {name}!")
    return HttpResponse("Контактна сторінка")
""")

    with open('mysite/pages/urls.py', 'w', encoding='utf-8') as f:
        f.write("""from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
""")

    with open('mysite/mysite/urls.py', 'w', encoding='utf-8') as f:
        f.write("""from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
]
""")

def analyze_settings(settings_path: str) -> dict:
    config = {}
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('DEBUG ='):
                    config['DEBUG'] = line.split('=')[1].strip()
                elif line.startswith('LANGUAGE_CODE ='):
                    config['LANGUAGE_CODE'] = line.split('=')[1].strip()
                elif line.startswith('TIME_ZONE ='):
                    config['TIME_ZONE'] = line.split('=')[1].strip()
                elif 'DATABASES' in line and '{' in line:
                    config['DATABASES'] = 'Налаштовано'
    except FileNotFoundError:
        pass
    return config

def check_security(settings_path: str) -> list[str]:
    warnings = []
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'DEBUG = True' in content:
                warnings.append("DEBUG = True (небезпечно для production)")
            if 'SECRET_KEY = ' in content and 'os.environ' not in content:
                warnings.append("SECRET_KEY захардкоджений")
            if "ALLOWED_HOSTS = []" in content:
                warnings.append("ALLOWED_HOSTS порожній")
    except FileNotFoundError:
        warnings.append(f"Файл {settings_path} не знайдено")
    return warnings

def main():
    setup_django_files()
    settings_path = 'mysite/mysite/settings.py'
    
    if not os.path.exists(settings_path):
        print(f"Файл {settings_path} не знайдено. Створіть Django-проект командою 'django-admin startproject mysite'.")
        sys.exit(1)

    config = analyze_settings(settings_path)
    print("=== Аналіз конфігурації Django ===\n")
    for key, value in config.items():
        print(f"  {key}: {value}")

    print("\n=== Перевірка безпеки ===\n")
    warnings = check_security(settings_path)
    if warnings:
        for w in warnings:
            print(f"  ⚠ {w}")
    else:
        print("  Попереджень не знайдено")

if __name__ == "__main__":
    main()