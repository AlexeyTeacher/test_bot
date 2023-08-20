# test_bot for yandex practicum
Тестовое наставника kids ai

Бот можно потыкать [тут](https://t.me/alexey_kirilov_test_bot)

## Задание 
Напиши на Python бота для Телеграм, который поможет нам с тобой познакомиться, задеплой его и пришли ссылку на работающего бота.
Функционал бота:

- посмотреть 1. твое последнее селфи и 2. фото из старшей школы
- прочитать небольшой пост о твоём главном увлечении
- прислать твой войс:
    - с рассказом в формате «объясняю своей бабушке», что такое GPT (до 1 минуты)
    - и максимально коротко объясни разницу между SQL и NoSQL (до 1 минуты)
    - история первой любви (до 1 минуты) — можно выдумать 🤫

Кроме этого, нужна команда, которая позволит получить нам ссылку на публичный репозиторий с исходниками этого бота.

Сделай часть команд кнопками, а часть — текстом.


## Решение 
Переменные окружения смотрите в `config.py`

### Как развернуть локально:
1. Создайте базу
2. Создайте директорию
3. Склонируйте проект
4. Создайте билд проекта
5. Запустите проект
### START Postgres
```bash
docker stop yandex_db || true && \
docker rm yandex_db || true && \
docker run -d --name yandex_db --restart always -p 5590:5432  \
     -e POSTGRES_DB=yandex \
     -e POSTGRES_USER=yandex \
     -e POSTGRES_PASSWORD=yandex \
     postgres -c shared_buffers=256MB 
```

### Сборка и запуск контейнера

```bash
docker build -t yandex_bot -f Dockerfile .
docker container rm -f yandex_bot || true && 
docker run --restart=always -d --name yandex_bot
       -e DB_HOST=local
       -e DB_PORT=5590
       -e DB_NAME=yandex
       -e DB_USER=yandex
       -e DB_PWD=yandex
       -e OWNER_LOGIN=<your telegram login>
       -e OWNER_NAME=<your telegram name>
       -e TKN=<your_token> 
       yandex_bot
```

## Бот можно потыкать [тут](https://t.me/alexey_kirilov_test_bot)
