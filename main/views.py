from django.core.cache import cache
from django.shortcuts import render

from main.dvagis import *


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def place(request):
    if request.method == 'POST':
        address = request.POST.get('inputAddress')
        name = request.POST.get('inputPlaceName')

        print(address)
        print(name)

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

        plus_start = summarization.find("**Плюсы:**")
        minus_start = summarization.find("**Минусы:**")

        # Извлекаем подстроки для плюсов и минусов
        pluses = summarization[plus_start:minus_start].strip().split('\n')[1:]
        minuses = summarization[minus_start:].strip().split('\n')[1:]

        print(pluses)

        for i in range(len(pluses)):
            pluses[i] = pluses[i].strip('*')
            if pluses[i] == '  ':
                pluses[i] = ''

        for i in range(len(minuses)):
            minuses[i] = minuses[i].strip('*')
            if minuses[i] == '  ':
                minuses[i] = ''

        # Если pluses[i] и minuses[i] пустые, то удаляем их со смещением индексов
        pluses = [i for i in pluses if i]
        minuses = [i for i in minuses if i]

        return render(request, 'reviews.html',
                      {'summarization': summarization, 'reviews': reviews, 'pluses': pluses, 'minuses': minuses})
