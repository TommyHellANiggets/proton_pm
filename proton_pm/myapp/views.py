from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages

def home(request):
    return render(request, 'terminal_hello.html')


def terminal(request):
    return render(request, 'terminal.html')


def load_photo(request):
    return render(request, 'load_photo.html')




def profile(request):
    # Получаем текущего пользователя
    current_user = request.user

    # Создаем контекст с данными профиля
    context = {
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
        'email': current_user.email,
        'role': 'Администратор' if current_user.is_staff else 'Оператор',

    }

    # Отрисовываем шаблон с переданным контекстом
    return render(request, 'profile.html', context)


def authorization(request):
    # Если запрос является POST, обрабатываем форму авторизации
    if request.method == 'POST':
        # Получаем данные из формы
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Проверяем учетные данные пользователя
        user = authenticate(request, username=username, password=password)

        # Если пользователь найден и учетные данные верные
        if user is not None:
            # Логиним пользователя
            login(request, user)
            # Перенаправляем пользователя на главную страницу или любую другую страницу
            return redirect('pages')  # Замените 'home' на нужный URL

        else:
            # Если учетные данные неверные, показываем сообщение об ошибке
            messages.error(request, 'Неверные учетные данные, попробуйте снова.')

    # Если запрос не POST, просто рендерим страницу авторизации
    return render(request, 'authorization.html')


def terminal_menu(request):
    return render(request, 'terminal_menu.html')


def terminal_career(request):
    return render(request, 'terminal_career.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Content, File
from .forms import ContentForm

import random
import string
import os

# Функция для генерации уникального URL
def generate_unique_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))

# Представление для обработки запросов и отображения файлов
@login_required
def pages(request):
    if request.method == 'POST':
        # Обработка формы ContentForm
        form = ContentForm(request.POST)
        if form.is_valid():
            # Получаем данные из формы
            parent_id = form.cleaned_data.get('parent_id')
            title = form.cleaned_data.get('title')

            # Проверяем, есть ли уже запись с таким parent_id и title
            if parent_id:
                existing_content = Content.objects.filter(parent_id=parent_id, title=title).exists()
                if not existing_content:
                    form.save()
            else:
                # Создаем объект Content, но не сохраняем его в базе данных
                content = form.save(commit=False)
                # Устанавливаем текущего пользователя как автора контента
                content.author = request.user
                # Сохраняем объект Content в базе данных
                content.save()

        # Обработка загрузки файлов
        if request.FILES:
            files = request.FILES.getlist('file')
            # Обработка всех файлов, переданных в запросе
            for file in files:
                # Создаем уникальный URL
                unique_url = generate_unique_url()

                # Убедитесь, что уникальный URL уникален в базе данных
                while File.objects.filter(unique_url=unique_url).exists():
                    unique_url = generate_unique_url()

                # Получите расширение файла
                file_extension = os.path.splitext(file.name)[1]  # Возвращает кортеж (basename, extension)

                # Переименуйте файл, используя уникальный URL и расширение файла
                new_file_name = unique_url + file_extension
                file.name = new_file_name

                # Создайте объект File с файлом, уникальным URL и расширением файла
                file_obj = File.objects.create(file=file, unique_url=unique_url, file_extension=file_extension)

                # Сохраните объект
                file_obj.save()

        # Перенаправление на ту же страницу после сохранения данных
        return redirect('pages')

    # Если запрос не POST, создаем пустую форму
    else:
        form = ContentForm()

    # Получаем все объекты Content из базы данных для отображения на странице
    all_content = Content.objects.all()
    # Получаем все загруженные файлы
    all_files = File.objects.all()

    # Формируем список допустимых родительских записей для выпадающего списка
    valid_parents = [content for content in all_content if not content.parent_id]

    context = {
        'form': form,
        'valid_parents': valid_parents,
        'all_content': all_content,
        'all_files': all_files,
    }

    # Отображаем страницу с текущими записями контента и загруженными файлами
    return render(request, 'pages.html', context)


from django.shortcuts import render, get_object_or_404
from .models import Content

def content_detail(request, content_id):
    content = get_object_or_404(Content, id=content_id)

    return render(request, 'terminal_created.html', {'contents': content})



from django.shortcuts import render, redirect
from .models import Content

def edit_child(request, child_id):
    child = Content.objects.get(id=child_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        child.title = title
        child.body = body
        child.save()
        return redirect('success_url')  # Перенаправить на страницу успешного сохранения
    return render(request, 'pages.html', {'child': child})
