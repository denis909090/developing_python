from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>Головна</h1><p>Опис проекту</p><ul><li>Пункт 1</li><li>Пункт 2</li><li>Пункт 3</li></ul>")

def about(request):
    return HttpResponse("Курс: Веб-розробка<br>ПР: 5<br>Студент: Ім'я Прізвище")

def contact(request):
    name = request.GET.get('name')
    if name:
        return HttpResponse(f"Привіт, {name}!")
    return HttpResponse("Контактна сторінка")
