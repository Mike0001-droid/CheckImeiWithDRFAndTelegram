# Owner avatar CheckImeiWithDRFAndTelegram
Телеграм бот IMEI
![GitHub top language](https://img.shields.io/github/languages/top/Mike0001-droid/CheckImeiWithDRFAndTelegram)


## Установка 
У вас должны быть установлены [зависимости проекта](https://github.com/Mike0001-droid/CheckImeiWithDRFAndTelegram/blob/main/requirements.txt)

1. Клонирование репозитория 

```git clone https://github.com/Mike0001-droid/CheckImeiWithDRFAndTelegram.git```

2. Создание виртуального окружения

```python -m venv venv```

3. Активация виртуального окружения

```cd venv/scripts/activate```

4. Установка зависимостей

```pip install -r requirements.txt```

5. Заполнение файла .env
   * Файл .env предназначен для хранения переменных окружения и должен выглядеть примерно так
     ![alt text](imageforreadme/env_example.png)

6. Запуск миграций

```python manage.py migrate```

7. Создание админа

```python manage.py createsuperuser```

8. Запуск сервера

```python manage.py runserver```


## Запуск бота

1. Переходим в директорию bot

```cd bot```

2. Запускаем файл aiogram_run.py

```python aiogram_run.py```


## Возможности сервиса

1. Проверка IMEI через API DRF 
    * Запускаем сервер Django
    * Переходим по адресу /api
    * Открываем приложение check и нажимаем зеленую кнопку Interact
      ![alt text](imageforreadme/checkimei.png)
    * Вставляем IMEI в форму и нажимаем синюю кнопку Send Request
      ![alt text](imageforreadme/send_request.png)

2. Авторизация по JWT - токену
    * Запускаем сервер Django
    * Переходим по адресу /api
    * Открываем приложение auth и нажимаем зеленую кнопку Interact
      ![alt text](imageforreadme/auth.png)
    * Кликаем на метод создания токена, вводим свои данные и нажимаем синюю кнопку Send Request
      ![alt text](imageforreadme/create_token.png)
    * Копируем access токен из результата запроса
      ![alt text](imageforreadme/response_auth.png)
    * В нижнем левом углу нажимаем на вкладку Authentication и нажимаем на token
      ![alt text](imageforreadme/auth_app.png)
    * Записываем в поле Scheme - Bearer, а в поле Token вставляем скопированный токен, затем нажимаем синюю кнопку Use Token Authentication
      ![alt text](imageforreadme/token.png)

3. Проверка IMEI через Telegram бота
    * Запускаем бота по инструкции выше
      ![alt text](imageforreadme/run_bot.png)
    * Используем команду /start
      ![alt text](imageforreadme/tg_start.png)
    * Вводим свой IMEI и получаем результат
      ![alt text](imageforreadme/tg_result.png)
    