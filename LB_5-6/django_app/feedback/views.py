from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import FeedbackForm


def home_page(request):
    context_data = {
        'page_title': 'Головна сторінка',
        'news_items': ['Оновлення системи', 'Нові правила', 'Знижки на послуги'],
        'active_users': 150,
    }
    return render(request, 'feedback/home.html', context_data)


def feedback_page(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Ваше повідомлення успішно надіслано!')
            return redirect('feedback')
    else:
        form = FeedbackForm()

    return render(request, 'feedback/form.html', {'form': form})
