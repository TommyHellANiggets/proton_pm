from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages

def home(request):
    return render(request, 'terminal_hello.html')


def terminal(request):
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
    return render(request, 'terminal.html', context)


def load_photo(request):
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
    return render(request, 'load_photo.html', context)





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

# Представление для обработки запросов и отображения файлов
@login_required
def pages(request):
    # Отрисовываем шаблон с переданным контекстом
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

    current_user = request.user

    objects_per_page = 1

    # Создаем объект Paginator для объектов Content
    paginator = Paginator(all_content, objects_per_page)

    # Получаем номер страницы из GET-параметра или устанавливаем первую страницу по умолчанию
    page_number = request.GET.get('page', 1)

    try:
        # Получаем запрошенную страницу
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # Если номер страницы не является целым числом, отображаем первую страницу
        page_obj = paginator.page(1)
    except EmptyPage:
        # Если номер страницы находится за пределами допустимых значений, отображаем последнюю страницу
        page_obj = paginator.page(paginator.num_pages)

    objects = Content.objects.all()

    # Создаем контекст с данными профиля
    context = {
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
        'email': current_user.email,
        'role': 'Администратор' if current_user.is_staff else 'Оператор',
        'form': form,
        'valid_parents': valid_parents,
        'all_content': all_content,
        'all_files': all_files,
        'items': objects,
        'page_obj': page_obj
    }

    # Отображаем страницу с текущими записями контента и загруженными файлами
    return render(request, 'pages.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .forms import RegistrationForm

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def settings(request):
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            username = registration_form.cleaned_data['username']
            first_name = registration_form.cleaned_data['first_name']
            last_name = registration_form.cleaned_data['last_name']
            email = registration_form.cleaned_data['email']
            password = registration_form.cleaned_data['password1']
            is_superuser = registration_form.cleaned_data['is_superuser']

            # Создаем нового пользователя
            new_user = User.objects.create_user(username=username,
                                                first_name=first_name,
                                                last_name=last_name,
                                                email=email,
                                                password=password)
            # Устанавливаем статус суперпользователя
            if is_superuser:
                new_user.is_superuser = True
                new_user.save()

            return redirect('settings')  # Перенаправляем обратно на страницу настроек


    else:
        registration_form = RegistrationForm()

    current_user = request.user

    # Создаем контекст с данными профиля
    context = {
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
        'email': current_user.email,
        'role': 'Администратор' if current_user.is_staff else 'Оператор',
    }

    users = User.objects.all()
    return render(request, 'settings.html', {'registration_form': registration_form, 'users': users, 'context': context})

@login_required
def delete_user(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(pk=user_id)
        user.delete()
        return redirect('settings')  # Перенаправляем обратно на страницу настроек
    else:
        return redirect('home')  # Возвращаемся на главную, если запрос не POST



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Content, File

@login_required
def save_file(request):
    if request.method == 'POST':
        files = request.FILES.getlist('file')
        for file in files:
            unique_url = generate_unique_url()
            while File.objects.filter(unique_url=unique_url).exists():
                unique_url = generate_unique_url()
            file_extension = file.name.split('.')[-1]
            new_file_name = unique_url + '.' + file_extension
            file.name = new_file_name
            file_obj = File.objects.create(file=file, unique_url=unique_url, file_extension=file_extension)
            file_obj.save()

            # Обновление изображений в контенте
            content_id = request.POST.get('content_id')
            if content_id:
                content = get_object_or_404(Content, pk=content_id)
                if len(files) == 1:
                    content.image1 = file_obj.file.url
                elif len(files) == 2:
                    content.image2 = file_obj.file.url
                elif len(files) == 3:
                    content.image1 = file_obj.file.url
                    content.image2 = file_obj.file.url
                    content.image3 = file_obj.file.url
                content.save()

    return redirect('pages')


def generate_unique_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))

@login_required
def update_content_images(request):
    if request.method == 'POST':
        content_id = request.POST.get('content_id')
        if Content.objects.filter(pk=content_id).exists():
            content = get_object_or_404(Content, pk=content_id)
            image1 = request.POST.get('image1')
            image2 = request.POST.get('image2')
            image3 = request.POST.get('image3')

            # Обновляем изображения в объекте Content
            content.image1 = image1
            content.image2 = image2
            content.image3 = image3
            content.save()

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Content matching query does not exist.'})




def content_detail(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    sub_contents = Content.objects.filter(parent_id=content_id)
    parent_content = get_object_or_404(Content, id=content_id)
    return render(request, 'terminal_created.html', {'content': content, 'sub_contents': sub_contents, 'parent_body': parent_content.body})


def content_detail_child(request, parent_id, content_id):
    content = get_object_or_404(Content, id=content_id)
    parent_content = get_object_or_404(Content, id=content_id)
    return render(request, 'terminal_created_child.html', {'content': content, 'parent_body': parent_content.body})

from django.shortcuts import render, redirect, get_object_or_404
import os

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Content

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Content
import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Content
import json

@login_required
def edit_content(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        content_id = request.POST.get('content_id')
        new_body = request.POST.get('body')
        image1 = request.POST.get('image1')
        image2 = request.POST.get('image2')
        image3 = request.POST.get('image3')

        content = get_object_or_404(Content, id=content_id)
        content.body = new_body

        # Сохраняем пути к загруженным файлам
        content.image1 = image1
        content.image2 = image2
        content.image3 = image3

        content.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'})

# def content_list(request):
#     # Извлекаем все записи из таблицы Content
#     contents = Content.objects.select_related('author').all()
#     # Передаем данные в шаблон
#     return render(request, 'pages.html', {'contents': contents})
from django.views.generic import ListView

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Content


@csrf_exempt
def delete_content(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content_id = data['id']
            content = Content.objects.get(id=content_id)
            content.delete()
            return JsonResponse({'success': True})
        except Content.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Content not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContentForm
from .models import Content
import random
import string

def generate_unique_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def create_or_edit_content(request, content_id=None):
    if content_id:
        content = get_object_or_404(Content, id=content_id)
    else:
        content = None

    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            content = form.save(commit=False)
            # Генерация уникального URL
            content.unique_url = generate_unique_url()
            content.save()
            return redirect('pages')  # Замени 'success_url' на URL страницы, которая должна отображаться после успешного сохранения контента
    else:
        form = ContentForm(instance=content)
    return render(request, 'pages.html', {'form': form})


from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

@login_required
@require_POST
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return JsonResponse({'status': 'success'}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'status': 'user not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
