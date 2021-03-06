# astra_linux_task
Task from astra linux
# Задача
Разработать приложение "Список задач" (ToDO).
Приложение должно уметь:
- Создавать/редактировать/удалять задачу
- Определять задаче крайний срок выполнения
- Отмечать задачу выполненной
- Вести историю изменения задачи
- Поддержка категорий и меток (тегов)
- Загружать данные по задачам из файлов (форматы Excel или CSV, на выбор кандидата)
- Выгружать данные по задачам в файл на локальный компьютер (форматы Excel или CSV, на выбор кандидата)
- Отправлять данные по задачам в виде файла (форматы Excel или CSV, на выбор кандидата) на ресурс http://qa-test.expsys.org:8080/upload-file

Описание метода загрузки файла на ресурс доступно по ссылке: http://qa-test.expsys.org:8080/swagger

# Требования к реализации
- Приложение должно быть web-ориентированным
- Приложение должно быть реализовано на Python версии не ниже 3.5 и Django REST Framework
- Взаимодействие приложения с HTTP сервером должно производиться архитектурным стилем взаимодействия REST
- СУБД для хранения данных может быть любым, на усмотрение кандидата

# Требования к выполнению задания
- Тестовое задание должно иметь сопроводительное письмо с описанием:
1. Общее описание реализованного приложения
2. Описание REST API приложения в формате OpenAPI 3
3. Инструкция по установке, настройке и запуску приложения
4. Предложения по дальнейшему развитию реализованного приложения
____
____
____
# Описание REST API приложения в формате OpenAPI 3
- Есть документация. После запуска сервера доступна по адресу [http://127.0.0.1:8000/swagger.json]
## Общее описание
Приложение для работа с todo. проектировалось по тестовому заданию. Включает в себя весь фукнционал из "задачи". 
## Все возможные операции
- /admin - Переход в админку django
- /api-auth - Аутентификация в API.
- /todos/ or / - Отображение всех задач
- /todos/<int:todo_id>/ - Перход на конкретную задачу
- /todos/export_to_csv/ - Скачивание Данных по задачам в формате CSV
- /todos/upload_file/ - Загрузка данных в модель Todo из CSV файла на локалькой машине
- /todos/send_file_to_remote/ - Отправка файла на удаленный сервер
- /todos/history/ - Отображение истории изменений задач
## Все возможные параметры
### /todos/ 

GET Запрос всех задач

POST создание новой задачи. Параметры {
        "task": str,
        "completed": bool,
        "timestamp": timestamp,
        "updated": timestamp,
        "id": int,
        "finish_date": date,
        "user": int,
        "category": str
}
Обязательный только 'task'
### /todos/<int:todo_id>/

GET Запрос конкретной задачи

PUT Обновление параметров задачи. Параметры {
        "task": str,
        "completed": bool,
        "timestamp": timestamp,
        "updated": timestamp,
        "id": int,
        "finish_date": date,
        "user": int,
        "category": str
}
Обязательный только 'task'

DELETE удаление задачи

### /todos/export_to_csv/

GET Скачивает файл с задачами на локальную машину

### /todos/upload_file/
POST Счкачивает данные из файла в модель django

{"file_name":str}

### /todos/send_file_to_remote/
POST Отправляет файл на удаленный сервер

{"file_name":str, "file_name_to_server":str, "url":str}

### /todos/history/
GET получение информации об изменениях в модели Todo

## Все возможные ответы
### */todos* или аналогично */todos/<int:todo_id>/*(Тут только один элемент выведется)
ответ:
[
{
        "task": str,
        "completed": bool,
        "timestamp": timestamp,
        "updated": timestamp,
        "id": int,
        "finish_date": date,
        "user": int,
        "category": str
}
]
### /todos/export_to_csv
Файл начнет скачиваться на локальную машину.


### /todos/upload_file
В Случае неверного пути. Статус ответа == 200

{
    "res": "Not found file",
    "Wrong path": "Todos.csv"
}

В Случае если данные из файла успешно добавлены. Статус ответа == 200

{
    "res": "File /home/oleg/Загрузки/Todos.csv added"
}

В Случае если данные не прошли валидацию. Статус == 400

{
    {"msg":"serializer"}
}

### /todos/send_file_to_remote
В Случае неверного пути. Статус ответа == 200

{
    "res": "Not found file",
    "Wrong path": "Todos.csv"
}

В Случае если данные из файла успешно добавлены на удаленный сервер. Статус ответа == 200

{
    "res": f"File {file_name}->{file_name_to_server} added to server {url}"
}

В Случае если данные не прошли валидацию. Статус == 400

{
    {"msg":"serializer"}
}

### /todos/history
возращается историю изменений. Статус ответа == 200
[
    {
        "model": "todo.historicaltodo",
        "pk": 27,
        "fields": {
            "id": 11,
            "task": "First",
            "timestamp": "2021-02-18T03:33:01.637Z",
            "completed": false,
            "updated": "2021-02-18T03:33:01.637Z",
            "finish_date": "2021-02-18",
            "user": null,
            "category": null,
            "history_date": "2021-02-18T03:33:01.639Z",
            "history_change_reason": null,
            "history_type": "+",
            "history_user": 1
        }
    },
 ]


# Инструкция по установке, настройке и запуску приложения

Инструкция по запуску через docker:
- Клонировать репозиторий
- Порт 8000 должен быть открыт на локальной машине
- Из директории проекта выполнить команду: sudo docker-compose --build -d api_todo
- Сервер будет доступен по: 127.0.0.1:8000
- Чтобы использовать методы API, нужно пройти аутентификацию. api-auth/login (admin:admin) 
- Чтобы не использовать admin:admin в качестве пользователя, можно создать пользователя самостоятельно.

Инструкция по запуску без docker(Linux Ubuntu):
- Клонировать репозиторий
- Создать виртуальную среду в корне проекта
- в качестве источника выбрать виртуальную среду которую создали (source env_name/bin/activate)
- Установить все требования, находясь в той же директории что и requirements.txt  python pip install -r requirements.txt
- Запустить сервер. Из директории где располагается manage.py выполнить python manage.py runserver
- Чтобы использовать методы API, нужно пройти аутентификацию. api-auth/login (admin:admin) 
- Чтобы не использовать admin:admin в качестве пользователя, можно создать пользователя самостоятельно.
# Предложения по дальнейшему развитию реализованного приложения
- Добавить тесты
- Добавить асинхронность
- Обработать крайние случаи
