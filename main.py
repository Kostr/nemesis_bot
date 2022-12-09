import os
import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv


load_dotenv()

bot = Bot(token=os.getenv("API_TOKEN"))
dp = Dispatcher(bot)

corporation2 = ['external/Корпорация - 2 - Инкубатор.png',
                'external/Корпорация - 2 - Материал для опытов.png']
corporation3 = corporation2 + ['external/Корпорация - 3 - Сторонний проект.png',
                               'external/Корпорация - 3 - Проверяя углы.png',
                               'external/Корпорация - 3 - Не оставляя следов.png']
corporation4 = corporation3 + ['external/Корпорация - 4 - Вклад в развитие.png',
                               'external/Корпорация - 4 - Нечестная игра.png']
corporation5 = corporation4 + ['external/Корпорация - 5 - Коллективное решение.png']
personal2 = ['external/Личная - 2 - Проверка систем.png']
personal3 = personal2 + ['external/Личная - 3 - Выгодное увольнение.png',
                         'external/Личная - 3 - Образцы материалов.png',
                         'external/Личная - 3 - Чумной Саркофаг.png']
personal4 = personal3 + ['external/Личная - 4 - Благодатные дары.png',
                         'external/Личная - 4 - Предупреждение.png']
personal5 = personal4 + ['external/Личная - 5 - Выжившие.png',
                         'external/Личная - 5 - Припоминая долги.png']

ALL_MISSIONS=False
if ALL_MISSIONS:
    original_corporation2 = ['original/Корпорация - 2 - Аутопсия.png',
                             'original/Корпорация - 2 - Моя прелесть.png',
                             'original/Корпорация - 2 - Подходящий момент для удара.png',
                             'original/Корпорация - 2 - Полевые исследования.png',
                             'original/Корпорация - 2 - Смерть в яйце.png',
                             'original/Корпорация - 2 - Ценный сотрудник.png']
    original_corporation3 = original_corporation2 + ['original/Корпорация - 3 - Старая вражда.png']
    original_corporation4 = original_corporation3 + ['original/Корпорация - 4 - Агрессивная политика.png']
    original_corporation5 = original_corporation4 + ['original/Корпорация - 5 - Озарение.png']
    original_personal2 = ['original/Личная - 2 - Барахольщик.png',
                          'original/Личная - 2 - В поисках истины.png',
                          'original/Личная - 2 - Великая охота.png',
                          'original/Личная - 2 - Достойные похороны.png',
                          'original/Личная - 2 - Карантин.png',
                          'original/Личная - 2 - Самое ценное.png']
    original_personal3 = original_personal2 + ['original/Личная - 3 - Старый друг.png']
    original_personal4 = original_personal3 + ['original/Личная - 4 - Лучшие друзья навсегда.png']
    original_personal5 = original_personal4 + ['original/Личная - 5 - Пришельцы на корабле.png']

    corporation2 += original_corporation2
    corporation3 += original_corporation3
    corporation4 += original_corporation4
    corporation5 += original_corporation5
    personal2 += original_personal2
    personal3 += original_personal3
    personal4 += original_personal4
    personal5 += original_personal5



inline_kb1 = InlineKeyboardMarkup(row_width=2)
inline_kb1.add(InlineKeyboardButton('Выбрать задание корпорации', callback_data='corporation_btn'))
inline_kb1.add(InlineKeyboardButton('Выбрать личную цель', callback_data='personal_btn'))

players = {}

class Player:
    def __init__(self, chat):
        self.name = None
        self.chat = chat
        self.corporate_mission_message = None
        self.personal_mission_message = None
        self.choice_message = None

@dp.message_handler(commands=['delete_messages'])
async def delete_messages(message: types.Message):
    for chat, p in players.items():
        if p.corporate_mission_message:
            await bot.delete_message(chat, p.corporate_mission_message.message_id)
            p.corporate_mission_message = None
        if p.personal_mission_message:
            await bot.delete_message(chat, p.personal_mission_message.message_id)
            p.personal_mission_message = None
        if p.choice_message:
            await bot.delete_message(chat, p.choice_message.message_id)
            p.choice_message = None

@dp.message_handler(commands=['send_mission_pick'])
async def send_mission_pick(message: types.Message):
    for chat, p in players.items():
        if not p.choice_message:
            print("Send mission picker to " + p.name)
            p.choice_message =  await bot.send_message(chat, "Выберите миссию:", reply_markup=inline_kb1) 

@dp.callback_query_handler(lambda c: c.data == 'corporation_btn')
@dp.callback_query_handler(lambda c: c.data == 'personal_btn')
async def personal_choice(call: types.CallbackQuery):
    player = players[call.from_user.id]
    print(player.name + " made his choice")
    if (call.data == 'corporation_btn'):
        await bot.delete_message(call.from_user.id, players[call.from_user.id].personal_mission_message.message_id)
        players[call.from_user.id].personal_mission_message = None
    elif (call.data == 'personal_btn'):
        await bot.delete_message(call.from_user.id, players[call.from_user.id].corporate_mission_message.message_id)
        players[call.from_user.id].corporate_mission_message = None
    await bot.delete_message(call.from_user.id, players[call.from_user.id].choice_message.message_id)
    players[call.from_user.id].choice_message = None

@dp.message_handler(commands=['send_missions'])
async def send_missions(message: types.Message):
    players_amount = len(players)
    if (players_amount == 2):
        corporation = corporation2
        personal = personal2
    elif (players_amount == 3):
        corporation = corporation3
        personal = personal3
    elif (players_amount == 4):
        corporation = corporation4
        personal = personal4
    elif (players_amount == 5):
        corporation = corporation5
        personal = personal5
    else:
        await message.answer("Error! players_amount = " + str(players_amount))
        return

    if (len(corporation) < players_amount):
        await message.answer("Error! not enough corporation missions for " + str(players_amount) + " players")
        return
    if (len(personal) < players_amount):
        await message.answer("Error! not enough personal missions for " + str(players_amount) + " players")
        return
   
    print(corporation) 
    print(personal) 
    corporate_missions = random.sample(corporation, players_amount)
    personal_missions = random.sample(personal, players_amount)
    game_misssions = list(zip(players, corporate_missions, personal_missions))
    
    i = 0
    for chat, p in players.items():
        photo = open("missions/" + corporate_missions[i], 'rb')
        if not p.corporate_mission_message:
            print("Send corporate mission to " + p.name + ': ' + corporate_missions[i])
            p.corporate_mission_message = await bot.send_photo(chat_id=chat, photo=photo)
        photo = open("missions/" + personal_missions[i], 'rb')
        if not p.personal_mission_message:
            print("Send personal mission to " + p.name + ': ' + personal_missions[i])
            p.personal_mission_message = await bot.send_photo(chat_id=chat, photo=photo)
        i += 1

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    if not message.chat.id in players:
        players[message.chat.id] = Player(message.chat)
        name = ""
        if "username" in message.chat:
            name += message.chat['username']
        if ("first_name" in message.chat) or ("last_name" in message.chat):
            name += " ("
            if "first_name" in message.chat:
                name += message.chat['first_name']
            if "last_name" in message.chat:
                name += ' ' + message.chat['last_name']
            name += ")"
        players[message.chat.id].name = name
        print(name + " has joined the game")

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
