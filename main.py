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

    def query(self, query):
        self.cursor.execute(query)

    def get_telegramID_tuple(self):
        self.query('select telegramID from Players')
        list = self.cursor.fetchall()
        listID =[]
        for i in list:
            listID.append(i['telegramID'])
        return listID

    def add_new_player(self, telegramID):
        self.cursor.execute('insert into Players(telegramID, state) values(%s, %s)', (telegramID, 'not_registered'))
        self.connection.commit()

    def get_All_players_All_info(self):
        self.cursor.execute('select playerID, telegramID, schoolNumber, mosregID, nic, placeId, forse, speed, state from Players')
        return self.cursor.fetchall()

    def get_state_from_id(self, player_id):
        self.query(f'select state from Players where playerID = {player_id}')
        return self.cursor.fetchall()

    def close_database(self):
        self.cursor.close()
        self.connection.close()

class Player():
    def __init__(self, telegramID):
        self.telegramID = telegramID
        db = Database()
        data = db.get_telegramID_tuple()
        print(data)
        if not telegramID in data:
            print('Неопознанный игрок')
            db.add_new_player(telegramID)
            data = db.get_All_players_All_info()
            print('Добавили игрока', data)
        else:
            print('Id телеграма есть в базе')
        print('Список ID telegram in DB:', data)
        self.playerID = 
        db.close_database()

    def get_state(self):
        db = Database()
        print(db)





    def add_user(self):
        pass
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
    text = 'Привет! Это игра "Школьные войны"! В этой игре ты моешь отстоять честь своей школы, захватывать дома и здания города Жуковского, объединяться с игроками из твоей школы и совместно месить конкурентоа из других школ.\n' \
           ''
    keyboard=aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    keyboard.add("Правила игры", "Регистрация")
    await message.reply(text, reply_markup=keyboard)

@dp.message_handler()
async def echo(message: aiogram.types.Message):
    state =''
    substate=''
    answer = ''

    await message.answer(message.text)

if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)