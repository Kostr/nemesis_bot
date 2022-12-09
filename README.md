# Описание

Телеграм-бот для выбора миссий к игре [Немезида](https://boardgamegeek.com/boardgame/167355/nemesis)

По материалам из [архива](https://disk.yandex.ru/d/DT4VaLJ5pnxDUw/4.%D0%94%D0%BE%D0%BF%D0%BE%D0%BB%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5%20%D0%BC%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D1%8B%20%D0%BE%D1%82%20%D0%A1%D0%BD%D0%B5%D0%B6%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%9B%D0%B8%D1%81%D0%B0/%D0%94%D0%BE%D0%BF%D0%BE%D0%BB%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5%20%D0%BC%D0%B8%D1%81%D1%81%D0%B8%D0%B8)

По умолчанию выдаёт только дополнительные миссии. Чтобы выдавал все, необходимо выставить `ALL_MISSIONS=True`

# Запуск бота

В директории необходимо создать файл `.env` с API токеном вашего личного бота в формате:
```
API_TOKEN='<token>'
```

После этого выполнить:
```
$ python -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ python main.py
```

# Команды

После старта бота каждый игрок должен выполнить команду `/start` (доступно через меню).

После этого все команды выполняет только мастер игры:

- `/send_missions` - отправит каждому игроку по 2 карты миссий

- `/send_mission_pick` - отправит каждому игроку по запросу на выбор миссии

- `/delete_messages` - удалит сообщения у всех игроков
