from django.core.cache import cache
from django.shortcuts import render

from main.dvagis import *


def index(request):
    return render(request, 'index.html')


def place(request):
    if request.method == 'POST':
        address = request.POST.get('inputAddress')
        name = request.POST.get('inputPlaceName')

        # Проверяем, есть ли данные в кэше
        cache_summarization_key = f"place_{address}_{name}"
        cache_rewiews_key = f"rewiews_{address}_{name}"
        summarization = cache.get(cache_summarization_key)
        reviews = cache.get(cache_rewiews_key)

        if summarization is None:
            # Если данных нет в кэше, выполняем запрос
            summarization, reviews = question_generation(address, name)

            # Сохраняем результат в кэше на определенное время
            cache.set(cache_summarization_key, summarization, timeout=60 * 60 * 24)
            cache.set(cache_rewiews_key, reviews, timeout=60 * 60 * 24)

        return render(request, 'reviews.html', {'summarization': summarization, 'reviews': reviews})
