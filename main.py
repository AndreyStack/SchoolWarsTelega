import logging

import aiogram
import pymysql.cursors

#states: не зарегистрирован, регистрация, откисает, в походе, в здании, крафтит ХП, прокачивает скорость, строит оборону,
#        в битве

# Connect to the database

class Database():
    def __init__(self):
        self.connection = pymysql.connect(host='server198.hosting.reg.ru',
                                     port=3306,
                                     user='u1917390_default',
                                     password='k5iZirj19JVFA0j5',
                                     database='u1917390_schoolwars',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()
    def get_All_players_All_info(self):
        self.cursor.execute('select playerID, telegramID, schoolNumber, mosregID, nic, placeId, forse, speed, state from Players')
        return self.cursor.fetchall()

    def get_all_telegramID_list(self):
        self.cursor.execute('select telegramID from Players')
        list = self.cursor.fetchall()
        listID =[]
        for i in list:
            listID.append(i['telegramID'])
        return listID

    def add_new_player(self, telegramID):
        self.cursor.execute('insert into Players(telegramID, state) values(%s, %s)',
                            (telegramID, 'not_registered'))
        self.connection.commit()
        self.cursor.execute(f'select playerID from Players where telegramID = {telegramID}')
        id = self.cursor.fetchone()['playerID']
        self.cursor.execute(f'update Players set nic = concat("Player", playerID) where telegramID = {telegramID}')
        self.connection.commit()


    def get_state_from_id(self, playerID):
        self.cursor.execute(f'select state from Players where playerID = {playerID}')
        return self.cursor.fetchone()['state']

    def set_state(self, playerID, new_state):
        self.cursor.execute(f'update Players set state' + new_state + ' where playerID = {playerID}')
        self.connection.commit()

    def get_playerID_from_telegramID(self, telegramID):
        self.cursor.execute(f'select playerID from Players where telegramID = {telegramID}')
        return self.cursor.fetchone()['playerID']



    def close_database(self):
        self.cursor.close()
        self.connection.close()
class State():
    not_registered = 'not_registered'
    registration = 'registration'
    wait_nic = 'wait_nic'
    choose_school = 'choose_school'


class Player():
    def __init__(self, telegramID):
        self.telegramID = telegramID
        db = Database()
        data = db.get_all_telegramID_list()
        if not telegramID in data:
            print('Неопознанный игрок')
            db.add_new_player(telegramID)
            data = db.get_All_players_All_info()
            print('Добавили игрока', data)
        else:
            print('Id телеграма есть в базе. Вот его данные: ', db.get_All_players_All_info())
        self.playerID = db.get_playerID_from_telegramID(self.telegramID)
        db.close_database()

    def get_state(self):
        db = Database()
        return db.get_state_from_id(self.playerID)

    def set_state(self, new_state):
        db = Database()
        db.set_state(self.playerID, new_state)

    def change_nic(self):
        pass

    def create_sqad(self):
        pass

    def join_to_sqad(self):
        pass

    def propos_atack(self):
        pass

    def vote(self):
        pass

    def craft_hp(self):
        pass

    def upgrade_speed(self):
        pass

    def get_info_near_places(self):
        pass


class Place():
    pass

API_TOKEN = '6114597666:AAEJt1XujLq1slzRE3CAOnyGCqJqSusjvaU'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = aiogram.Bot(token=API_TOKEN)
dp = aiogram.Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: aiogram.types.Message):
    print(aiogram.types.User.get_current())
    player = Player(aiogram.types.User.get_current()['id'])
    print('Создан объект: ', player.playerID, player.telegramID, player.get_state())
    text = 'Привет! Это игра "Школьные войны"! В этой игре ты моешь отстоять честь своей школы, захватывать дома и здания города Жуковского, объединяться с игроками из твоей школы и совместно месить конкурентоа из других школ.\n'
    keyboard=aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    if player.get_state() == State.not_registered:
        text = text + '\n Для игры необходимо пройти регистрацию.'
        keyboard.add("Правила игры", "Регистрация")
    await message.reply(text, reply_markup=keyboard)

@dp.message_handler()
async def echo(message: aiogram.types.Message):
    player = Player(aiogram.types.User.get_current()['id'])
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    text = ''
    if message.text == "Регистрация":
        text = 'Для регистрации необходимо выбрать себе погоняло и номер школы за которую будете играть '
        player.set_state(State.registration)
        keyboard.add('Введите погоняло', 'Выберите свою школу')

    if message.text == 'Введите погоняло' and player.get_state() == State.registration:
        text = "Введите свое погоняло для игры и нажмите отправить"
        player.set_state(State.wait_nic)
    await message.answer(text)

if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)