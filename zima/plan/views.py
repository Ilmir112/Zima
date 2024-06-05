import asyncio
import subprocess
import os
import requests
import zipfile
import psycopg2

import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.decorators import login_required
from multiprocessing import Process


from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django import forms

from .forms import CustomUserCreationForm

class MyLoginView(LoginView):
    template_name = 'registration/login.html'


    # Вывод хоста базы данных PostgreSQL

    def form_valid(self, form):
        # Проверяем, есть ли у пользователя доступ
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        print(f'gtgt{username}')
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:

            login(self.request, user)
            # postgres_conn_user = {
            #     'database': 'users2',
            #     'user': 'postgres',
            #     'password': '195375AsD+',
            #     'host': '176.109.99.210',
            #     'port': '5432'
            # }
            #
            # self.user_datas(username, postgres_conn_user)
            return redirect('home')  # Перенаправление на главную страницу
        else:
            # В случае неудачной авторизации выводим сообщение об ошибке
            form.add_error(None, 'Неправильное имя пользователя или пароль')
            return self.form_invalid(form)

    def user_datas(self, username, postgres_conn_user):
        conn = psycopg2.connect(**postgres_conn_user)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username, last_name, first_name, patronymic, position, organization FROM plan_krs_customuser "
            "WHERE username=(%s)", (username,))
        user_login = cursor.fetchone()
        print(user_login)
        conn.commit()
        conn.close()
        conn2 = psycopg2.connect(**postgres_conn_user)
        cursor2 = conn2.cursor()
        cursor2.execute(
            "INSERT INTO plan_krs_employee ("
            "last_name, first_name, middle_name, position, organization) VALUES (%s, %s, %s, %s, %s)",
            (user_login[1:]))
        conn2.commit()
        conn2.close()


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # Перенаправление на главную страницу
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('home')  # Перенаправить на главную страницу
#     else:
#         form = AuthenticationForm()
#     return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Перенаправить на главную страницу
    else:
        form = AuthenticationForm()
    return render(request, 'registration/logout.html', {'form': form})

@login_required
def home(request):
    return render(request, 'home.html')

def run_exe_zima(request):
    download_and_cache_zima_app(request)
    try:
        subprocess.Popen("tmp\ZIMA\ZIMA.exe", shell=True)  # Замените на путь к вашему исполняемому файлу
        return redirect('home')
    except Exception as e:
        return HttpResponse(f"Error: {e}")

def download_and_cache_zima_app(request):
    version_app = get_version_from_json()
    # Получаем версию приложения из источника (например, из GitHub)
    response = requests.get('https://api.github.com/repos/Ilmir112/Create_work_krs/releases/latest')
    latest_version = response.json()['tag_name']
    print(latest_version)

    if version_app != latest_version:  # Проверяем, если версии не совпадают
        url = f"https://github.com/Ilmir112/Create_work_krs/releases/download/{latest_version}/ZIMA.zip"
        # Вызываем запрос только при наличии новой версии
        response = requests.get(url)

        update_version(latest_version)

        with open("zima.zip", "wb") as file:  # Сохраняем архив в папку tmp
            file.write(response.content)

        extract_dir = "tmp"

        with zipfile.ZipFile("zima.zip", 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        # Путь к папке "tmp"
        folder_path = os.path.abspath("tmp")

        # Открываем папку "tmp" в проводнике Windows
        subprocess.Popen(f'explorer "{folder_path}"')

        os.remove("zima.zip")


        return HttpResponse("PyQt5 app cached successfully")
    else:
        return HttpResponse(f"Текущая версия {version_app}")


def get_version_from_json():
    with open('version_app.json', 'r') as file:
        data = json.load(file)
        version_app = data['version']
        print(version_app)
    return version_app

def update_version(new_version):
    with open('version_app.json', 'r') as file:
        data = json.load(file)
        data['version'] = new_version

    with open('version_app.json', 'w') as file:
        json.dump(data, file)


