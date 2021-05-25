import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random

import addition.data_doc_addition
import NumberGame, Weather, City, Words

vk_session = vk_api.VkApi(
    token='ffcaa658692c13d6c1bf5fe7946572169e6c4fb1c76ca4e8aef0fb4ddf60ae95e97210da8d6b677df6fb6')
longpoll = VkBotLongPoll(vk_session, '199196587')

flag = False
flag_play = False
words_add_d, id_add_sp, wait_answ = {}, [],  False
gl_add_word = ['', '']

id_d = dict()

print('start')


def main():
    print('in function')
    global flag, flag_play, id_d, words_add_d, id_add_sp, gl_add_word, wait_answ
    for event in longpoll.listen():

        vk = vk_session.get_api()
        if event.type == VkBotEventType.MESSAGE_NEW and \
                event.obj.message['from_id'] not in id_d.keys():
            id_d[event.obj.message['from_id']] = {'flag': False,
                                                  'flag_play': False,
                                                  'number_game': False,
                                                  'numb_gm_polz': False,
                                                  # 'numb_gm_p_cl': None,
                                                  'numb_gm_ii': False,
                                                  'find_highest': False,
                                                  # 'numb_gm_ii_cl': None,
                                                  'weather_fl': False,
                                                  'time_fl': False,
                                                  'city_fl_pr': False,
                                                  'lg_lt_city': [],
                                                  'this_moment': False,
                                                  'certain_time': False,
                                                  'ct_parts': [],
                                                  'words_game': [False, None, None],
                                                  'words_r_find': False,
                                                  'all_last_let': None,
                                                  'one_let': None,
                                                  'words': {},
                                                  'add_word': '',
                                                  'help': [True, False, False,
                                                           False, False, False,
                                                           False, False, False,
                                                           False, False, False,
                                                           False, False, False,
                                                           False, False, False,
                                                           False, False, False,
                                                           ]}
            print('new user')
            text = "Для начала работы напишите 'Начать'"

            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=text,
                             keyboard=open('.\keyboard_start.json', 'r',
                                           encoding='UTF-8').read(),
                             random_id=random.randint(0, 2 ** 64))

        elif event.type == VkBotEventType.MESSAGE_NEW and \
                event.obj.message['text'].lower() == 'начать' \
                and not id_d[event.obj.message['from_id']]['flag']:

            id_d[event.obj.message['from_id']]['flag'] = True   # запуск бота

            id_d[event.obj.message['from_id']]['help'][0] = False   # подсказка для запускающей бот фразы
            id_d[event.obj.message['from_id']]['help'][1] = True   # подсказка на выбор навыка

            print(event)
            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])

            vk.messages.send(user_id=event.obj.message['from_id'],
                             message="Привет, я бот < имя >!\n" \
                                     "Вот мои навыки:\n"
                                     "✅ Игры\n" \
                                     "✅ Погода\n" \
                                     "✅ Время\n" \
                                     "✅ Карты\n" \
                                     "✅ Удача\n" \
                                     "Если Вы хотите очистить историю сообщений, напишите - ❌ ОЧИСТИТЬ ИСТОРИЮ ❌",
                             keyboard=open('keyboard\keyboard_menu.json', 'r',
                                           encoding='UTF-8').read(),
                             attachment=random.choice(
                                 addition.data_doc_addition.attachment_doc_add['hi']),
                             random_id=random.randint(0, 2 ** 64))


        elif event.type == VkBotEventType.MESSAGE_NEW and 'игр' in \
            event.obj.message['text'].lower() and id_d[event.obj.message['from_id']]['flag'] and \
                not(id_d[event.obj.message['from_id']]['number_game'] or
                id_d[event.obj.message['from_id']]['words_game'][0] or
                id_d[event.obj.message['from_id']]['weather_fl'] or
                id_d[event.obj.message['from_id']]['time_fl']):   # обработка запуска навыка "игры"

            id_d[event.obj.message['from_id']]['flag_play'] = True   # флаг-запуск навыка "игры"

            id_d[event.obj.message['from_id']]['help'][1] = False   # подсказка на выбор навыка
            id_d[event.obj.message['from_id']]['help'][2] = True   # подсказка на выбор игры

            vk.messages.send(user_id=event.obj.message['from_id'],
                             message="Можем поиграть в:\n"
                                     "○ Камень-ножницы-бумага\n"
                                     "○ Угадай число\n"
                                     "○ Слова\n"
                                     "○ Быки - коровы\n",
                             keyboard=open('keyboard\keyboard_games.json', 'r',
                                           encoding='UTF-8').read(),
                             attachment=random.choice(
                                 addition.data_doc_addition.attachment_doc_add[
                                     'game']),
                             random_id=random.randint(0, 2 ** 64))

        elif event.type == VkBotEventType.MESSAGE_NEW and 'угадай число' in  \
                event.obj.message['text'].lower() and \
                id_d[event.obj.message['from_id']]['flag_play']:

            id_d[event.obj.message['from_id']]['number_game'] = True   # флаг-запуск игры "угадай число"

            id_d[event.obj.message['from_id']]['help'][2] = False  # подсказка на выбор игры
            id_d[event.obj.message['from_id']]['help'][3] = True  # подсказка на выбор игрока, делающего первый ход

            text = "Название: Угадай число\n" \
                   "Один из нас - Я или ВЫ - загадывает число от 1 до 999.\n" \
                   "Другой начинает угадывать, называя числа, " \
                   "получая в ответ фразы 'больше' или 'меньше'.\n" \
                   "○ 'Меньше' - загаданное число меньше Вашего.\n" \
                   "○ 'Больше' - загаданное число больше Вашего.\n" \
                   "○ 'Стоп' - если хотите завершить игру\n" \
                   "⚪ Кто загадывает число: Я или ВЫ?" \

            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=text,
                             keyboard=open('keyboard\keyboard_i_y_stop.json', 'r',
                                           encoding='UTF-8').read(),
                             attachment=random.choice(
                                 addition.data_doc_addition.attachment_doc_add['number']),
                             random_id=random.randint(0, 2 ** 64))

        elif event.type == VkBotEventType.MESSAGE_NEW and \
                id_d[event.obj.message['from_id']]['number_game'] and \
                event.obj.message['text'].lower() == 'я':

            id_d[event.obj.message['from_id']]['help'][3] = False  # подсказка на выбор игрока, делающего первый ход
            id_d[event.obj.message['from_id']]['numb_gm_polz'] = True   # флаг-маркер выбронного режима игры "угадай число"

            numb_gm_p_cl = NumberGame.NumberGamePolz(
                id_d[event.obj.message['from_id']]['number_game'],
                id_d[event.obj.message['from_id']]['numb_gm_polz'], True)

            text = "Хорошо. Загадывайте число.\n" \
                   "Загадали? ДА / НЕТ"

            id_d[event.obj.message['from_id']]['help'][4] = True   # подсказка-опрос о том, загадал ли игрок число или нет

            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=text,
                             keyboard=open('keyboard\keyboard_y_n.json', 'r', encoding='UTF-8').read(),
                             random_id=random.randint(0, 2 ** 64))

        elif event.type == VkBotEventType.MESSAGE_NEW and \
                id_d[event.obj.message['from_id']]['numb_gm_polz'] and \
                event.obj.message['text'].lower() in ['нет', 'да']:
                # id_d[event.obj.message['from_id']]['number_game'] and \

            if event.obj.message['text'].lower() == 'нет':
                text = "Ладно, я могу подождать.\n" \
                       "А теперь загадали? ДА / НЕТ"

                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 keyboard=open('keyboard\keyboard_y_n.json', 'r', encoding='UTF-8').read(),
                                 attachment=random.choice(
                                     addition.data_doc_addition.attachment_doc_add['time']),
                                 random_id=random.randint(0, 2 ** 64))

            else:
                id_d[event.obj.message['from_id']]['help'][4] = False  # подсказка-опрос о том, загадал ли игрок число или нет
                id_d[event.obj.message['from_id']]['help'][5] = True  # подсказка о вводе ответа "больше", "меньше" или "равно"

                text = "Хорошо. Начинаю угадывать\n"
                text_1, keyboard = numb_gm_p_cl.number_game_st()

                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 random_id=random.randint(0, 2 ** 64))

                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text_1,
                                 keyboard=keyboard,
                                 random_id=random.randint(0, 2 ** 64))

        elif event.type == VkBotEventType.MESSAGE_NEW and event.obj.message[
            'text'].lower() in ['больше', 'меньше', 'равно'] and \
                id_d[event.obj.message['from_id']]['numb_gm_polz']:
                # id_d[event.obj.message['from_id']]['flag'] \
                # id_d[event.obj.message['from_id']]['number_game'] and \
            if numb_gm_p_cl.minim < numb_gm_p_cl.maxim - 1:

                id_d[event.obj.message['from_id']]['help'][5], \
                id_d[event.obj.message['from_id']]['help'][8], keyboard, \
                text = numb_gm_p_cl.numb_game_plz_func(event.obj.message['text'].lower())

                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 keyboard=keyboard,
                                 random_id=random.randint(0, 2 ** 64))
            else:
                text = "Должно быть, Вы ошиблись.\n" \
                       "Такого числа нет в диапазоне от 1 до 1000"

                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 keyboard=open('keyboard\keyboard_start_notstart.json',
                                               'r', encoding='UTF-8').read(),
                                 random_id=random.randint(0, 2 ** 64))

        elif event.type == VkBotEventType.MESSAGE_NEW and \
                id_d[event.obj.message['from_id']]['number_game'] and \
                event.obj.message['text'].lower() == 'вы':

            id_d[event.obj.message['from_id']]['help'][3] = False  # подсказка на выбор игрока, делающего первый ход
            id_d[event.obj.message['from_id']]['help'][6] = True  # подсказка на ввод максимально возможного загаданного ботом числа

            id_d[event.obj.message['from_id']]['numb_gm_ii'] = True  # флаг-маркер выбронного режима игры "угадай число"
            id_d[event.obj.message['from_id']]['find_highest'] = False  # флаг-маркер о вводе максимально возможного загаданного числа для бота

            numb_gm_ii_cl = NumberGame.NumberGameII(
                id_d[event.obj.message['from_id']]['number_game'],
                id_d[event.obj.message['from_id']]['numb_gm_ii'],
                id_d[event.obj.message['from_id']]['find_highest'],
                False)

            text = "Введите максимальное число, которое мне можно загадать\n" \
                   "Минимальное число - 0"

            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=text,
                             keyboard=open('keyboard\keyboard_stop.json',
                                           'r', encoding='UTF-8').read(),
                             random_id=random.randint(0, 2 ** 64))

        elif event.type == VkBotEventType.MESSAGE_NEW and \
                id_d[event.obj.message['from_id']]['numb_gm_ii'] and \
                event.obj.message['text'].isdigit():
                # and id_d[event.obj.message['from_id']]['number_game'] and \
                # id_d[event.obj.message['from_id']]['flag']

            id_d[event.obj.message['from_id']]['help'][6] = False   # подсказка на ввод максимально возможного загаданного ботом числа

            if not id_d[event.obj.message['from_id']]['find_highest']:

                id_d[event.obj.message['from_id']]['number_game'], \
                id_d[event.obj.message['from_id']]['numb_gm_ii'], \
                id_d[event.obj.message['from_id']]['find_highest'], \
                id_d[event.obj.message['from_id']]['help'][7], text = \
                    numb_gm_ii_cl.highest(event.obj.message['text'].lower())

                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 keyboard=open('keyboard\keyboard_stop.json', 'r',
                                               encoding='UTF-8').read(),
                                 random_id=random.randint(0, 2 ** 64))

            else:
                text, id_d[event.obj.message['from_id']]['help'][7], \
                id_d[event.obj.message['from_id']]['help'][8], keyboard = \
                    numb_gm_ii_cl.numb_game_ii_func(event.obj.message['text'].lower())

                if keyboard:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     keyboard=open('keyboard\keyboard_start_notstart.json', 'r',
                                                   encoding='UTF-8').read(),
                                     random_id=random.randint(0, 2 ** 64))

                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     keyboard=open('keyboard\keyboard_stop.json', 'r',
                                         encoding='UTF-8').read(),
                                     random_id=random.randint(0, 2 ** 64))

        elif event.type == VkBotEventType.MESSAGE_NEW and event.obj.message['text'].lower() in \
                ['погода', 'время'] and not (id_d[event.obj.message['from_id']]['weather_fl'] and \
                    id_d[event.obj.message['from_id']]['time_fl']) and id_d[event.obj.message['from_id']]['flag']:

            if not id_d[event.obj.message['from_id']]['weather_fl'] and \
                    not id_d[event.obj.message['from_id']]['time_fl']:

                if event.obj.message['text'].lower() == 'погода':
                    id_d[event.obj.message['from_id']]['weather_fl'] = True   # флаг-запуск навыка "погода\время" в режиме "погода"
                else:

                    id_d[event.obj.message['from_id']]['time_fl'] = True   # флаг-запуск навыка "время"
                    print(id_d[event.obj.message['from_id']])

                id_d[event.obj.message['from_id']]['city_fl_pr'] = True   # флаг-маркер процесса определения искомого города

                id_d[event.obj.message['from_id']]['help'][1] = False   # подсказка на выбор навыка
                id_d[event.obj.message['from_id']]['help'][9] = True  # подсказка на ввод названия города

                text = "С радостью Вам помогу! Введите название города, данные " \
                       "для которого Вы хотели бы получить.\n" \
                       "Для выхода напишите СТОП"

                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 keyboard=open('keyboard\keyboard_stop.json', 'r',
                                               encoding='UTF-8').read(),
                                 attachment=random.choice(addition.data_doc_addition.attachment_doc_add[
                                         'planet']),
                                 random_id=random.randint(0, 2 ** 64))

        elif event.type == VkBotEventType.MESSAGE_NEW and (id_d[event.obj.message['from_id']]['weather_fl'] or \
            id_d[event.obj.message['from_id']]['time_fl']) and id_d[event.obj.message['from_id']]['city_fl_pr'] and \
                id_d[event.obj.message['from_id']]['flag'] and \
                event.obj.message['text'].lower() != 'стоп':

                city = event.obj.message['text'].lower()

                city_cl = City.City(event.obj.message['text'].lower())

                if len(city_cl.search(city)) == 3:

                    id_d[event.obj.message['from_id']]['lg_lt_city'] = city_cl.search(city)   # список из координат города, его названия

                    id_d[event.obj.message['from_id']]['help'][9] = False  # подсказка на ввод названия города
                    id_d[event.obj.message['from_id']]['help'][10] = True   # подсказка-уточнение названия искомого города

                    text = f"Вы хотите получить данные о городе {id_d[event.obj.message['from_id']]['lg_lt_city'][2]}?\n" \
                        "ДА или НЕТ\n"

                    id_d[event.obj.message['from_id']]['city_fl_pr'] = False   # флаг-маркер процесса определения искомого города

                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     keyboard=open('keyboard\keyboard_y_n.json', 'r',
                                         encoding='UTF-8').read(),
                                     attachment=random.choice(addition.data_doc_addition.attachment_doc_add['city']),
                                     random_id=random.randint(0, 2 ** 64))
                    print('yesno', id_d[event.obj.message['from_id']])
                else:
                    text = city_cl.search(city)

                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     random_id=random.randint(0, 2 ** 64))

        elif event.type == VkBotEventType.MESSAGE_NEW and event.obj.message[
            'text'].lower() in ['да', 'нет'] and not (id_d[event.obj.message['from_id']]['city_fl_pr'] or id_d[event.obj.message['from_id']]['ct_parts']) and \
                (id_d[event.obj.message['from_id']]['weather_fl'] or id_d[event.obj.message['from_id']]['time_fl']) and \
                event.obj.message['text'].lower() not in ['данный момент', 'определенное время']:

            id_d[event.obj.message['from_id']]['help'][10] = False   # подсказка-уточнение названия искомого города

            if event.obj.message['text'].lower() == 'да':
                if id_d[event.obj.message['from_id']]['weather_fl']:

                    id_d[event.obj.message['from_id']]['help'][11] = True   # подсказка о выборе пользователем временного промежутка

                    text = "Прогноз погоды на:\n" \
                           "○ Данный момент\n" \
                           "○ Определенное время\n"

                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     keyboard=open('keyboard\keyboard_now_parts.json', 'r',
                                         encoding='UTF-8').read(),
                                     random_id=random.randint(0, 2 ** 64))
                else:
                    id_d[event.obj.message['from_id']]['help'][1] = True   # подсказка на выбор навыка
                    id_d[event.obj.message['from_id']]['time_fl'] = True   # флаг-запуск навыка "погода\время" в режиме "время"

                    weather_cl = Weather.Weather(id_d[event.obj.message['from_id']]['lg_lt_city'][2], False,
                                                 id_d[event.obj.message['from_id']]['lg_lt_city'][1],
                                                 id_d[event.obj.message['from_id']]['lg_lt_city'][0],
                                                 id_d[event.obj.message['from_id']]['weather_fl'])

                    text = weather_cl.response_d('')

                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     random_id=random.randint(0, 2 ** 64))

                    id_d[event.obj.message['from_id']]['weather_fl'] = False  # флаг-запуск навыка "погода\время" в режиме "погода"
                    id_d[event.obj.message['from_id']]['time_fl'] = False  # флаг-запуск навыка "погода\время" в режиме "время"
                    id_d[event.obj.message['from_id']]['city_fl_pr'] = False  # флаг-маркер процесса определения искомого города
                    id_d[event.obj.message['from_id']]['lg_lt_city'] = []  # список из координат города, его названия

                    text = "Выберите один из навыков:\n" \
                           "✅ Игры\n" \
                           "✅ Погода\n" \
                           "✅ Время\n" \
                           "✅ Карты\n" \
                           "✅ Удача\n"

                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     keyboard=open(
                                         'keyboard\keyboard_menu.json', 'r',
                                         encoding='UTF-8').read(),
                                     random_id=random.randint(0, 2 ** 64))

            else:
                id_d[event.obj.message['from_id']]['city_fl_pr'] = True  # флаг-маркер процесса определения искомого города
                id_d[event.obj.message['from_id']]['help'][9] = True   # подсказка на ввод названия города

                text = "Повторите ввод названия города"

                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 random_id=random.randint(0, 2 ** 64))

        elif event.type == VkBotEventType.MESSAGE_NEW and (event.obj.message[
            'text'].lower() in ['данный момент', 'определенное время'] or \
                event.obj.message['text'].lower() in id_d[event.obj.message['from_id']]['ct_parts']) and \
                id_d[event.obj.message['from_id']]['weather_fl'] and not id_d[event.obj.message['from_id']]['city_fl_pr']:

            id_d[event.obj.message['from_id']]['help'][11] = False  # подсказка о выборе пользователем временного промежутка

            if event.obj.message['text'].lower() == 'данный момент':
                id_d[event.obj.message['from_id']]['help'][1] = True  # подсказка на выбор навыка

                if not id_d[event.obj.message['from_id']]['this_moment']:
                    id_d[event.obj.message['from_id']]['this_moment'] = True   # режим "данный момент" в навыке "погода\время"

                weather_cl = Weather.Weather(id_d[event.obj.message['from_id']]['lg_lt_city'][2],
                                             id_d[event.obj.message['from_id']]['this_moment'],
                                             id_d[event.obj.message['from_id']]['lg_lt_city'][1],
                                             id_d[event.obj.message['from_id']]['lg_lt_city'][0],
                                     id_d[event.obj.message['from_id']]['weather_fl'])

                text = weather_cl.response_d('')

                vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     random_id=random.randint(0, 2 ** 64))

                id_d[event.obj.message['from_id']]['weather_fl'] = False  # флаг-запуск навыка "погода\время" в режиме "погода"
                id_d[event.obj.message['from_id']]['this_moment'] = False  # режим "данный момент" в навыке "погода\время"
                id_d[event.obj.message['from_id']]['city_fl_pr'] = False  # флаг-маркер процесса определения искомого города
                id_d[event.obj.message['from_id']]['lg_lt_city'] = []   # список из координат города, его названия
                print(id_d[event.obj.message['from_id']])

                text = "Выберите один из навыков:\n" \
                       "✅ Игры\n" \
                       "✅ Погода\n" \
                       "✅ Время\n" \
                       "✅ Карты\n" \
                       "✅ Удача\n"

                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 keyboard=open('keyboard\keyboard_menu.json',
                                               'r',
                                               encoding='UTF-8').read(),
                                 random_id=random.randint(0, 2 ** 64))

            if (event.obj.message['text'] == 'Определенное время') or \
                    (id_d[event.obj.message['from_id']]['certain_time'] and \
                     event.obj.message['text'].lower() in id_d[event.obj.message['from_id']]['ct_parts']):

                id_d[event.obj.message['from_id']]['help'][12] = True  # подсказка о выборе пользователем временного промежутка(режим "определенное время")

                if not id_d[event.obj.message['from_id']]['certain_time']:
                    id_d[event.obj.message['from_id']]['certain_time'] = True   # режим "определенное время" в навыке "погода\время"

                    weather_cl = Weather.Weather(id_d[event.obj.message['from_id']]['lg_lt_city'][2],
                                                 id_d[event.obj.message['from_id']]['this_moment'],
                                                 id_d[event.obj.message['from_id']]['lg_lt_city'][1],
                                                 id_d[event.obj.message['from_id']]['lg_lt_city'][0],
                                         id_d[event.obj.message['from_id']]['weather_fl'])

                    # список из названий временных промежутков для вывода данных в навыке "погода"(режим "определенное время")
                    text, id_d[event.obj.message['from_id']]['ct_parts'] = weather_cl.response_d('')

                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     random_id=random.randint(0, 2 ** 64))

                else:
                    id_d[event.obj.message['from_id']]['help'][12] = False   # подсказка о выборе пользователем временного промежутка(режим "определенное время")
                    id_d[event.obj.message['from_id']]['help'][1] = True   # подсказка на выбор навыка

                    weather_cl = Weather.Weather(id_d[event.obj.message['from_id']]['lg_lt_city'][2],
                                                 id_d[event.obj.message['from_id']]['this_moment'],
                                                 id_d[event.obj.message['from_id']]['lg_lt_city'][1],
                                                 id_d[event.obj.message['from_id']]['lg_lt_city'][0],
                                         id_d[event.obj.message['from_id']]['weather_fl'])

                    text_1, text_2 = weather_cl.response_d(event.obj.message['text'])

                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text_1,
                                     random_id=random.randint(0, 2 ** 64))
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text_2,
                                     random_id=random.randint(0, 2 ** 64))

                    id_d[event.obj.message['from_id']]['weather_fl'] = False  # флаг-запуск навыка "погода\время" в режиме "погода"
                    id_d[event.obj.message['from_id']]['city_fl_pr'] = False   # флаг-маркер процесса определения искомого города
                    id_d[event.obj.message['from_id']]['lg_lt_city'] = []   # список из координат города, его названия
                    id_d[event.obj.message['from_id']]['certain_time'] = True   # режим "определенное время" в навыке "погода\время"
                    # список из названий временных промежутков для вывода данных в навыке "погода"(режим "определенное время")
                    id_d[event.obj.message['from_id']]['ct_parts']: []

                    print('погода 500', id_d[event.obj.message['from_id']])

                    text = "Выберите один из навыков:\n" \
                           "✅ Игры\n" \
                           "✅ Погода\n" \
                           "✅ Время\n" \
                           "✅ Карты\n" \
                           "✅ Удача\n"

                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     keyboard=open(
                                         'keyboard\keyboard_menu.json', 'r',
                                         encoding='UTF-8').read(),
                                     random_id=random.randint(0, 2 ** 64))

        elif event.type == VkBotEventType.MESSAGE_NEW and 'слова' in \
                event.obj.message['text'].lower() and \
                id_d[event.obj.message['from_id']]['flag_play']:

            id_d[event.obj.message['from_id']]['words_game'][0] = True   # флаг-запуск игры "слова"

            id_d[event.obj.message['from_id']]['help'][2] = False   # подсказка на выбор игры
            id_d[event.obj.message['from_id']]['help'][18] = True   # подсказка-опрос, о начале игры(игра «Слова»)
            print("слова 524", id_d[event.obj.message['from_id']]['help'])

            text = "Название: Игра в слова\n" \
                   "Правила очень просты! Вы называете любое слово,\n" \
                   "а я называю слово, первая буква которого совпадает с" \
                   " последней буквой Вашего слова.\n" \
                   "Если названо слово, заканчивающееся на Й, Ы, Ъ, Ь,\n" \
                   " следующему игроку нужно придумать слово на предпоследню" \
                   " букву.\n" \
                   "Слова в процессе однного кона игры не должны повторяться.\n" \
                   "Нельзя использовать имена прилагательные и имена собственные.\n" \
                   "○ Если во время игры Вы не знаете слово" \
                   " или надоело играть - напишите СТОП\n" \
                   "✅ Для продолжения напишите ДА\n" \
                   "❎ Если не хотите играть - НЕТ\n"

            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=text,
                             keyboard=open('keyboard\keyboard_y_n.json', 'r',
                                           encoding='UTF-8').read(),
                             attachment=random.choice(addition.data_doc_addition.attachment_doc_add[
                                     'words']),
                             random_id=random.randint(0, 2 ** 64))

        elif event.type == VkBotEventType.MESSAGE_NEW and event.obj.message['text'].lower() \
                in ['да', 'нет'] and id_d[event.obj.message['from_id']]['words_game'][0] and \
            not id_d[event.obj.message['from_id']]['words_game'][1]:

            if event.obj.message['text'].lower() == 'да':

                id_d[event.obj.message['from_id']]['help'][18] = False   # подсказка-опрос, о начале игры(игра «Слова»)
                id_d[event.obj.message['from_id']]['help'][13] = True   # подсказка-запрос выбора режима игры(игра «Слова»)
                id_d[event.obj.message['from_id']]['words_r_find'] = True  # флаг-поиск режима "на одну букву/ на все буквы"(игра «Слова»)

                text = 'Мы с Вами будем играть в слова на ' \
                       'одну букву или на все буквы алфавита?'
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 keyboard=open('keyboard\keyboard_all_one.json', 'r',
                                               encoding='UTF-8').read(),
                                 random_id=random.randint(0, 2 ** 64))
            else:
                id_d[event.obj.message['from_id']]['help'][18] = False  # подсказка-опрос, о начале игры(игра «Слова»)
                id_d[event.obj.message['from_id']]['help'][1] = True  # подсказка на выбор навыка
                id_d[event.obj.message['from_id']]['words_game'][0] = False  # флаг-запуск игры "слова"

                print(id_d[event.obj.message['from_id']])

                text = "Выберите один из навыков:\n" \
                       "✅ Игры\n" \
                       "✅ Погода\n" \
                       "✅ Время\n" \
                       "✅ Карты\n" \
                       "✅ Удача\n"

                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 keyboard=open('keyboard\keyboard_menu.json','r',
                                               encoding='UTF-8').read(),
                                 random_id=random.randint(0, 2 ** 64))

        elif event.type == VkBotEventType.MESSAGE_NEW and event.obj.message['text'].lower() \
                in ['на одну букву', 'на все буквы'] and id_d[event.obj.message['from_id']]['words_game'][0] and \
                not id_d[event.obj.message['from_id']]['words_game'][1] and \
                id_d[event.obj.message['from_id']]['words_r_find']:

            id_d[event.obj.message['from_id']]['words_r_find'] = False  # флаг-поиск режима "на одну букву/ на все буквы"(игра «Слова»)

            if event.obj.message['text'].lower() == 'на одну букву':

                id_d[event.obj.message['from_id']]['words_game'][1] = 'one'
                # id_d[event.obj.message['from_id']]['words_one_f'] = True # флаг-поиск буквы на которую будут начинаться слова

                id_d[event.obj.message['from_id']]['help'][13] = False   # подсказка-запрос выбора режима игры(игра «Слова»)
                id_d[event.obj.message['from_id']]['help'][14] = True   # подсказка-запрос о вводе буквы, на которую должны начинаться слова(игра «Слова»)

                text = 'Назовите букву, на которую должны начинаться все слова'
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 random_id=random.randint(0, 2 ** 64))
            else:
                id_d[event.obj.message['from_id']]['words_game'][1] = 'all'
                id_d[event.obj.message['from_id']]['help'][13] = False  # подсказка-запрос выбора режима игры(игра «Слова»)
                id_d[event.obj.message['from_id']]['help'][15] = True  # подсказка, кто начинает игру(игра «Слова»)

                text = 'Кто начинает - Я или ВЫ ?'
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 keyboard=open('keyboard\keyboard_i_y_stop.json', 'r',
                                     encoding='UTF-8').read(),
                                 random_id=random.randint(0, 2 ** 64))

        elif event.type == VkBotEventType.MESSAGE_NEW and event.obj.message['text'].lower() \
                in 'абвгдеёжзийклмнопрстуфхцчшщэюя' and id_d[event.obj.message['from_id']]['words_game'][0] and \
                 id_d[event.obj.message['from_id']]['words_game'][1] == 'one' and not \
                id_d[event.obj.message['from_id']]['one_let']:

            id_d[event.obj.message['from_id']]['help'][14] = False  # подсказка-запрос о вводе буквы, на которую должны начинаться слова(игра «Слова»)
            id_d[event.obj.message['from_id']]['help'][15] = True  # подсказка, кто начинает игру(игра «Слова»)

            id_d[event.obj.message['from_id']]['one_let'] = event.obj.message['text'].lower()

            text = 'Кто начинает - Я или ВЫ ?'
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=text,
                             keyboard=open(
                                 'keyboard\keyboard_i_y_stop.json', 'r',
                                 encoding='UTF-8').read(),
                             random_id=random.randint(0, 2 ** 64))

        elif event.type == VkBotEventType.MESSAGE_NEW and event.obj.message[
            'text'].lower() in ['я', 'вы'] and id_d[event.obj.message['from_id']]['words_game'][0] and \
                id_d[event.obj.message['from_id']]['words_game'][1]:

            if event.obj.message['text'].lower() == 'я':

                id_d[event.obj.message['from_id']]['words_game'][2] = 'polz'

                id_d[event.obj.message['from_id']]['help'][15] = False  # подсказка, кто начинает игру(игра «Слова»)
                id_d[event.obj.message['from_id']]['help'][16] = True   # подсказка, о вводе первого слова на нужную букву(игра «Слова»)

                print(id_d[event.obj.message['from_id']]['help'])

                if id_d[event.obj.message['from_id']]['words_game'][1] == 'one':
                    text = f"Назовите слово на букву {id_d[event.obj.message['from_id']]['one_let']}"
                else:
                    text = 'Назовите слово на любую букву(кроме ь, ъ, ы)'

                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 keyboard=open('keyboard\keyboard_stop.json', 'r',
                                     encoding='UTF-8').read(),
                                 random_id=random.randint(0, 2 ** 64))
            else:
                id_d[event.obj.message['from_id']]['help'][15] = False  # подсказка, кто начинает игру(игра «Слова»)
                id_d[event.obj.message['from_id']]['help'][17] = True  # подсказка, о вводе слова на нужную букву(игра «Слова»)

                id_d[event.obj.message['from_id']]['words_game'][2] = 'ii'
                text = 'Хорошо, я начну'
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 random_id=random.randint(0, 2 ** 64))

                if id_d[event.obj.message['from_id']]['words_game'][1] == 'one':

                    id_d[event.obj.message['from_id']]['help'][8], k, etc = \
                        Words.WordsGame().find_word(id_d[event.obj.message['from_id']]['words'],
                                                    id_d[event.obj.message['from_id']]['one_let'], True, '')
                else:
                    id_d[event.obj.message['from_id']]['help'][8], k, etc = \
                        Words.WordsGame().find_word(id_d[event.obj.message['from_id']]['words'], '', False, '')

                print(etc)

                if id_d[event.obj.message['from_id']]['words_game'][1] == 'all':

                    word, id_d[event.obj.message['from_id']]['all_last_let'] = etc
                    text = f"Мое слово: {word}\n" \
                                f"Назовите слово на букву {id_d[event.obj.message['from_id']]['all_last_let']}"
                else:
                    word, id_d[event.obj.message['from_id']]['one_let'] = etc
                    text = f"Мое слово: {word}\n" \
                            f"Назовите слово на букву {id_d[event.obj.message['from_id']]['one_let']}"

                id_d[event.obj.message['from_id']]['words'][word[0]] = []
                id_d[event.obj.message['from_id']]['words'][word[0]].append(word)
                print(id_d[event.obj.message['from_id']]['words'])

                vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     keyboard=k,
                                     random_id=random.randint(0, 2 ** 64))

                id_d[event.obj.message['from_id']]['words_game'][2] = 'polz'

        elif event.type == VkBotEventType.MESSAGE_NEW and id_d[event.obj.message['from_id']]['flag'] and \
                id_d[event.obj.message['from_id']]['words_game'][0] and \
                (id_d[event.obj.message['from_id']]['words_game'][1] == 'all' or \
                 (id_d[event.obj.message['from_id']]['words_game'][1] == 'one' and \
                         id_d[event.obj.message['from_id']]['one_let'])) and \
                event.obj.message['text'].lower() != 'стоп' and \
                event.obj.message['text'].lower() not in ['добавить слово', 'добавить'] and \
                event.obj.message['text'].lower()[0] in 'абвгдеёчжзийклмнопрстуфхцчшщэюя' and \
                id_d[event.obj.message['from_id']]['words_game'][2] and not \
                (id_d[event.obj.message['from_id']]['help'][8] or \
                 id_d[event.obj.message['from_id']]['help'][19]):
                # id_d[event.obj.message['from_id']]['words_game'][2] == 'polz' and \

                if event.obj.message['text'].lower()[0] not in [id_d[event.obj.message['from_id']]['one_let'],
                                                                id_d[event.obj.message['from_id']]['all_last_let']] and \
                        any([id_d[event.obj.message['from_id']]['one_let'],
                             id_d[event.obj.message['from_id']]['all_last_let']]):

                    if id_d[event.obj.message['from_id']]['one_let']:
                        text = f"Вы должны назвать слово на букву {id_d[event.obj.message['from_id']]['one_let']}"
                    else:
                        text = f"Вы должны назвать слово на букву {id_d[event.obj.message['from_id']]['all_last_let']}"
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     random_id=random.randint(0, 2 ** 64))

                elif event.obj.message['text'].lower()[0] in id_d[event.obj.message['from_id']]['words'].keys() and \
                        event.obj.message['text'].lower() in id_d[event.obj.message['from_id']]['words'][event.obj.message['text'].lower()[0]]:

                    if id_d[event.obj.message['from_id']]['words_game'][1] == 'all':
                        text = f"Слово: {event.obj.message['text'].lower()} уже было использовано\n" \
                            f"Назовите слово на букву {id_d[event.obj.message['from_id']]['all_last_let']}"
                    else:
                        text = f"Слово: {event.obj.message['text'].lower()} уже было использовано\n" \
                            f"Назовите слово на букву {id_d[event.obj.message['from_id']]['one_let']}"
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     keyboard=k,
                                     random_id=random.randint(0, 2 ** 64))
                else:
                    print(words_add_d)
                    if event.obj.message['from_id'] in words_add_d.keys() and \
                            event.obj.message['text'].lower() in words_add_d[event.obj.message['from_id']]:

                        text = f'''Слово {event.obj.message['text'].lower()} добавлено в список Ваших предложений для улучшения игры\n'''\
                            f'''Назовите другое слово на букву {event.obj.message['text'].lower()[0]}'''

                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=text,
                                         keyboard=open('keyboard\keyboard_stop.json','r',
                                             encoding='UTF-8').read(),
                                         random_id=random.randint(0, 2 ** 64))
                    else:
                        if id_d[event.obj.message['from_id']]['words_game'][1] == 'one':

                            id_d[event.obj.message['from_id']]['help'][8], k, etc = \
                                Words.WordsGame().check_word(event.obj.message['text'].lower(),
                                                             id_d[event.obj.message['from_id']]['words'],
                                                             id_d[event.obj.message['from_id']]['one_let'])

                        else:
                            id_d[event.obj.message['from_id']]['help'][8], k, etc = \
                                Words.WordsGame().check_word(event.obj.message['text'].lower(),
                                                             id_d[event.obj.message['from_id']]['words'],f_let='')
                        print(etc)
                        if len(etc) == 2:
                            if event.obj.message['text'].lower()[0] not in id_d[event.obj.message['from_id']]['words'].keys():

                                id_d[event.obj.message['from_id']]['words'][event.obj.message['text'].lower()[0]] = []

                            id_d[event.obj.message['from_id']]['words'][event.obj.message['text'].lower()[0]].append(event.obj.message['text'].lower())

                            if id_d[event.obj.message['from_id']]['words_game'][1] == 'all':
                                word, id_d[event.obj.message['from_id']]['all_last_let'] = etc

                                if word[0] not in id_d[event.obj.message['from_id']]['words'].keys():

                                    id_d[event.obj.message['from_id']]['words'][word[0]] = []

                                text = f"Мое слово: {word}\n" \
                                    f"Назовите слово на букву {id_d[event.obj.message['from_id']]['all_last_let']}"
                            else:
                                word, id_d[event.obj.message['from_id']]['one_let'] = etc

                                text = f"Мое слово: {word}\n" \
                                    f"Назовите слово на букву {id_d[event.obj.message['from_id']]['one_let']}"

                            id_d[event.obj.message['from_id']]['words'][word[0]].append(word)

                            print(id_d[event.obj.message['from_id']]['words'])

                            print(word)
                            print(id_d[event.obj.message['from_id']]['words_game'][1])
                            id_d[event.obj.message['from_id']]['help'][16] = False   # подсказка, о вводе первого слова на нужную букву(игра «Слова»)
                            id_d[event.obj.message['from_id']]['help'][17] = True  # подсказка, о вводе слова на нужную букву(игра «Слова»)

                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             message=text,
                                             keyboard=k,
                                             random_id=random.randint(0, 2 ** 64))

                        else:
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             message=etc,
                                             keyboard=k,
                                             random_id=random.randint(0, 2 ** 64))
                            if not id_d[event.obj.message['from_id']]['help'][8]:

                                id_d[event.obj.message['from_id']]['add_word'] = event.obj.message['text'].lower()
                                text = 'Для внесения слова в наши базы нажмите "Добавить слово"'

                                id_d[event.obj.message['from_id']]['help'][17] = False  # подсказка, о вводе слова на нужную букву(игра «Слова»)
                                id_d[event.obj.message['from_id']]['help'][19] = True   # подсказка-опрос, хочет ли пользователь предложить добавить слово и БД или нет(игра «Слова»)

                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=text,
                                                 keyboard=open('keyboard\keyboard_add_stop.json', 'r',
                                                     encoding='UTF-8').read(),
                                                 random_id=random.randint(0, 2 ** 64))

        elif event.type == VkBotEventType.MESSAGE_NEW and \
                event.obj.message['text'].lower() == 'перезапустить' and \
                id_d[event.obj.message['from_id']]['help'][8]:

            if id_d[event.obj.message['from_id']]['numb_gm_polz']:

                id_d[event.obj.message['from_id']]['help'][8] = False   # подсказка о вводе ответа "перезапустить"\"не перезапускать"
                id_d[event.obj.message['from_id']]['numb_gm_polz'] = False   # флаг-маркер выбронного режима игры "угадай число"

                id_d[event.obj.message['from_id']]['number_game'] = True  # флаг-запуск игры "угадай число"

                id_d[event.obj.message['from_id']]['help'][2] = False  # подсказка на выбор игры
                id_d[event.obj.message['from_id']]['help'][3] = True  # подсказка на выбор игрока, делающего первый ход

                text = "⚪ Кто загадывает число: Я или ВЫ?"
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 keyboard=open('keyboard\keyboard_i_y_stop.json', 'r',
                                             encoding='UTF-8').read(),
                                 attachment=random.choice(addition.data_doc_addition.attachment_doc_add[
                                                 'number']),
                                 random_id=random.randint(0, 2 ** 64))

            if id_d[event.obj.message['from_id']]['numb_gm_ii']:

                print(id_d[event.obj.message['from_id']])

                id_d[event.obj.message['from_id']]['help'][8] = False  # подсказка о вводе ответа "перезапустить"\"не перезапускать"
                id_d[event.obj.message['from_id']]['numb_gm_ii'] = False  # флаг-маркер выбронного режима игры "угадай число"
                id_d[event.obj.message['from_id']]['find_highest'] = False  # флаг-маркер о вводе максимально возможного загаданного числа для

                id_d[event.obj.message['from_id']]['number_game'] = True  # флаг-запуск игры "угадай число"

                id_d[event.obj.message['from_id']]['help'][2] = False  # подсказка на выбор игры
                id_d[event.obj.message['from_id']]['help'][3] = True  # подсказка на выбор игрока, делающего первый ход

                text = "⚪ Кто загадывает число: Я или ВЫ?"

                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 keyboard=open('keyboard\keyboard_i_y_stop.json', 'r',
                                               encoding='UTF-8').read(),
                                 attachment=random.choice(addition.data_doc_addition.attachment_doc_add[
                                                              'number']),
                                 random_id=random.randint(0, 2 ** 64))

            if id_d[event.obj.message['from_id']]['words_game'][0]:

                print(id_d[event.obj.message['from_id']])

                id_d[event.obj.message['from_id']]['words_game'][0] = [True, None, None]  # флаг-запуск игры "слова"
                                                                                        # режим игры(игра «Слова»)
                                                                                        # кто начинет(игра «Слова»)

                id_d[event.obj.message['from_id']]['words_r_find'] = False  # флаг-поиск режима "на одну букву/ на все буквы"(игра «Слова»)

                id_d[event.obj.message['from_id']]['all_last_let'] = None  # буква на которую должно начинаться слово("на все буквы"/(игра «Слова»))
                id_d[event.obj.message['from_id']]['one_let'] = None  # буква на которую должно начинаться слово("на одну букву"(игра «Слова»))

                id_d[event.obj.message['from_id']]['words'] = {}  # словарь с названными словами(игра «Слова»)

                id_d[event.obj.message['from_id']]['help'][13] = True  # подсказка-запрос выбора режима игры(игра «Слова»)

                id_d[event.obj.message['from_id']]['help'][14] = False  # подсказка-запрос о вводе буквы, на которую должны начинаться слова(игра «Слова»)
                id_d[event.obj.message['from_id']]['help'][15] = False  # подсказка, кто начинает игру(игра «Слова»)
                id_d[event.obj.message['from_id']]['help'][16] = False  # подсказка, о вводе первого слова на нужную букву(игра «Слова»)
                id_d[event.obj.message['from_id']]['help'][17] = False  # подсказка, о вводе слова на нужную букву(игра «Слова»)
                id_d[event.obj.message['from_id']]['help'][18] = False  # подсказка-опрос, о начале игры(игра «Слова»)
                print(id_d[event.obj.message['from_id']])

                text = 'Мы с Вами будем играть в слова на ' \
                       'одну букву или на все буквы алфавита?'
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 keyboard=open('keyboard\keyboard_all_one.json','r',
                                               encoding='UTF-8').read(),
                                 random_id=random.randint(0, 2 ** 64))

        elif event.type == VkBotEventType.MESSAGE_NEW and \
                event.obj.message['text'].lower() == 'не перезапускать' and \
                id_d[event.obj.message['from_id']]['help'][8]:

            if id_d[event.obj.message['from_id']]['numb_gm_polz']:

                id_d[event.obj.message['from_id']]['help'][8] = False  # подсказка о вводе ответа "перезапустить"\"не перезапускать"
                id_d[event.obj.message['from_id']]['help'][1] = True  # подсказка на выбор навыка

                id_d[event.obj.message['from_id']]['number_game'] = False  # флаг-запуск игры "угадай число"
                id_d[event.obj.message['from_id']]['numb_gm_polz'] = False  # флаг-маркер выбронного режима игры "угадай число"

            if id_d[event.obj.message['from_id']]['numb_gm_ii']:

                id_d[event.obj.message['from_id']]['help'][8] = False  # подсказка о вводе ответа "перезапустить"\"не перезапускать"
                id_d[event.obj.message['from_id']]['help'][1] = True  # подсказка на выбор навыка

                id_d[event.obj.message['from_id']]['number_game'] = False  # флаг-запуск игры "угадай число"
                id_d[event.obj.message['from_id']]['numb_gm_ii'] = False  # флаг-маркер выбронного режима игры "угадай число"

            if id_d[event.obj.message['from_id']]['words_game'][0]:

                print(id_d[event.obj.message['from_id']])

                id_d[event.obj.message['from_id']]['help'][8] = False  # подсказка о вводе ответа "перезапустить"\"не перезапускать"
                id_d[event.obj.message['from_id']]['help'][1] = True  # подсказка на выбор навыка

                id_d[event.obj.message['from_id']]['words_game'] = [False, None, None]  # флаг-запуск игры "слова"
                                                                                           # режим игры(игра «Слова»)
                                                                                           # кто начинет(игра «Слова»)

                id_d[event.obj.message['from_id']]['words_r_find'] = False   # флаг-поиск режима "на одну букву/ на все буквы"(игра «Слова»)

                id_d[event.obj.message['from_id']]['all_last_let'] = None   # буква на которую должно начинаться слово("на все буквы"/(игра «Слова»))
                id_d[event.obj.message['from_id']]['one_let'] = None   # буква на которую должно начинаться слово("на одну букву"(игра «Слова»))

                id_d[event.obj.message['from_id']]['words'] = {}  # словарь с названными словами(игра «Слова»)

                print(id_d[event.obj.message['from_id']])

            text = "Выберите один из навыков:\n" \
                   "✅ Игры\n" \
                   "✅ Погода\n" \
                   "✅ Время\n" \
                   "✅ Карты\n" \
                   "✅ Удача\n"

            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=text,
                             keyboard=open('keyboard\keyboard_menu.json', 'r',
                                           encoding='UTF-8').read(),
                             random_id=random.randint(0, 2 ** 64))

        elif event.type == VkBotEventType.MESSAGE_NEW and \
                event.obj.message['text'].lower() == 'стоп':

            if id_d[event.obj.message['from_id']]['number_game']:

                id_d[event.obj.message['from_id']]['number_game'] = False  # флаг-запуск игры "угадай число"
                id_d[event.obj.message['from_id']]['numb_gm_polz'] = False  # флаг-маркер выбронного режима игры "угадай число"
                id_d[event.obj.message['from_id']]['numb_gm_ii'] = False  # флаг-маркер выбронного режима игры "угадай число"

                id_d[event.obj.message['from_id']]['help'][3] = False  # подсказка на выбор игрока, делающего первый ход
                id_d[event.obj.message['from_id']]['help'][4] = False   # подсказка-опрос о том, загадал ли игрок число или нет
                id_d[event.obj.message['from_id']]['help'][5] = False  # подсказка о вводе ответа "больше", "меньше" или "равно"

                id_d[event.obj.message['from_id']]['help'][6] = False  # подсказка на ввод максимально возможного загаданного ботом числа
                id_d[event.obj.message['from_id']]['help'][7] = False  # подсказка о вводе угадываемого пользователем числа

            if id_d[event.obj.message['from_id']]['weather_fl'] or \
                    id_d[event.obj.message['from_id']]['time_fl']:

                id_d[event.obj.message['from_id']]['weather_fl'] = False  # флаг-запуск навыка "погода\время" в режиме "погода"
                id_d[event.obj.message['from_id']]['city_fl_pr'] = False  # флаг-маркер процесса определения искомого города
                id_d[event.obj.message['from_id']]['lg_lt_city'] = []  # список из координат города, его названия
                id_d[event.obj.message['from_id']]['certain_time'] = False  # режим "определенное время" в навыке "погода\время"

                # список из названий временных промежутков для вывода данных в навыке "погода"(режим "определенное время")
                id_d[event.obj.message['from_id']]['ct_parts']: []
                id_d[event.obj.message['from_id']]['this_moment'] = False  # режим "данный момент" в навыке "погода\время"
                id_d[event.obj.message['from_id']]['time_fl'] = False  # флаг-запуск навыка "погода\время" в режиме "время"

            if id_d[event.obj.message['from_id']]['words_game'][0]:

                print(id_d[event.obj.message['from_id']])

                id_d[event.obj.message['from_id']]['words_game'] = [False, None, None]  # флаг-запуск игры "слова"
                                                                                           # режим игры(игра «Слова»)
                                                                                           # кто начинет(игра «Слова»)

                id_d[event.obj.message['from_id']]['words_r_find'] = False   # флаг-поиск режима "на одну букву/ на все буквы"(игра «Слова»)

                id_d[event.obj.message['from_id']]['all_last_let'] = None   # буква на которую должно начинаться слово("на все буквы"/(игра «Слова»))
                id_d[event.obj.message['from_id']]['one_let'] = None   # буква на которую должно начинаться слово("на одну букву"(игра «Слова»))

                id_d[event.obj.message['from_id']]['words'] = {}  # словарь с названными словами(игра «Слова»)

                id_d[event.obj.message['from_id']]['help'][13] = False   # подсказка-запрос выбора режима игры(игра «Слова»)
                id_d[event.obj.message['from_id']]['help'][14] = False   # подсказка-запрос о вводе буквы, на которую должны начинаться слова(игра «Слова»)
                id_d[event.obj.message['from_id']]['help'][15] = False   # подсказка, кто начинает игру(игра «Слова»)
                id_d[event.obj.message['from_id']]['help'][16] = False   # подсказка, о вводе первого слова на нужную букву(игра «Слова»)
                id_d[event.obj.message['from_id']]['help'][17] = False   # подсказка, о вводе слова на нужную букву(игра «Слова»)
                id_d[event.obj.message['from_id']]['help'][18] = False   # подсказка-опрос, о начале игры(игра «Слова»)
                print(id_d[event.obj.message['from_id']])

            id_d[event.obj.message['from_id']]['help'][1] = True  # подсказка на выбор навыка

            text = "Выберите один из навыков:\n" \
                   "✅ Игры\n" \
                   "✅ Погода\n" \
                   "✅ Время\n" \
                   "✅ Карты\n" \
                   "✅ Удача\n"

            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=text,
                             keyboard=open('keyboard\keyboard_menu.json', 'r',
                                           encoding='UTF-8').read(),
                             random_id=random.randint(0, 2 ** 64))
            print(id_d[event.obj.message['from_id']])

        elif event.type == VkBotEventType.MESSAGE_NEW and \
                id_d[event.obj.message['from_id']]['flag'] and \
                id_d[event.obj.message['from_id']]['words_game'][0] and \
                (id_d[event.obj.message['from_id']]['words_game'][1] == 'all' or \
                 (id_d[event.obj.message['from_id']]['words_game'][1] == 'one' and \
                  id_d[event.obj.message['from_id']]['one_let'])) and \
                event.obj.message['text'].lower() != 'стоп' and \
                event.obj.message['text'].lower() in ['добавить слово', 'не добавлять слово'] and \
                id_d[event.obj.message['from_id']]['words_game'][2] and not \
                id_d[event.obj.message['from_id']]['help'][8]:

            id_d[event.obj.message['from_id']]['help'][17] = True
            # подсказка, о вводе слова на нужную букву(игра «Слова»)
            id_d[event.obj.message['from_id']]['help'][19] = False
            # подсказка-опрос, хочет ли пользователь предложить добавить слово и БД или нет(игра «Слова»)

            if event.obj.message['text'].lower() == 'добавить слово':
                if event.obj.message['from_id'] not in id_add_sp:
                    id_add_sp.append(event.obj.message['from_id'])
                    words_add_d[event.obj.message['from_id']] = []

                words_add_d[event.obj.message['from_id']].append(id_d[event.obj.message['from_id']]['add_word'])

                if gl_add_word == ['', '']:
                    gl_add_word[0], gl_add_word[1] = event.obj.message['from_id'], id_d[event.obj.message['from_id']]['add_word']

                if not wait_answ:
                    id = random.choice(id_add_sp)
                    id_d[event.obj.message['from_id']]['add_word'] = words_add_d[id][0]

                    text = f'''Пользователь {id} хочет добавить слово \n
                    💡{id_d[event.obj.message['from_id']]['add_word']}💡'''
                    '''Добавить / Не добавлять'''

                    wait_answ = True
                    vk.messages.send(peer_id='2000000001',
                                     message=text,
                                     keyboard=open('keyboard\keyboard_add_not.json','r',
                                                   encoding='UTF-8').read(),
                                     random_id=random.randint(0, 2 ** 64))

                text = "Спасибо за Ваше предложение! \n"\
                "Оно будет рассмотрено в ближайшие сроки"

                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 random_id=random.randint(0, 2 ** 64))

            if id_d[event.obj.message['from_id']]['one_let']:
                text = f"Продолжаем игру! \nВы должны назвать слово на букву {id_d[event.obj.message['from_id']]['one_let']}"
            else:
                text = f"Продолжаем игру! \nВы должны назвать слово на букву {id_d[event.obj.message['from_id']]['all_last_let']}"
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=text,
                             random_id=random.randint(0, 2 ** 64))


        elif words_add_d and not wait_answ:
            print('спрашиваю')
            id = random.choice(id_add_sp)
            id_d[event.obj.message['from_id']]['add_word'] = words_add_d[id][0]

            text = f'''Пользователь {id} хочет добавить слово \n
            💡{id_d[event.obj.message['from_id']]['add_word']}💡'''
            '''Добавить / Не добавлять'''

            wait_answ = True
            vk.messages.send(peer_id='2000000001',
                             message=text,
                             keyboard=open('keyboard\keyboard_add_not.json','r',
                                           encoding='UTF-8').read(),
                             random_id=random.randint(0, 2 ** 64))

        elif event.type == VkBotEventType.MESSAGE_NEW and \
                id_d[event.obj.message['from_id']]['flag'] and \
                id_d[event.obj.message['from_id']]['words_game'][0] and \
                (id_d[event.obj.message['from_id']]['words_game'][1] == 'all' or \
                 (id_d[event.obj.message['from_id']]['words_game'][1] == 'one' and \
                  id_d[event.obj.message['from_id']]['one_let'])) and \
                event.obj.message['text'].lower() != 'стоп' and \
                ('добавить' in event.obj.message['text'].lower() or \
                 'не добавлять' in event.obj.message['text'].lower()) and \
                id_d[event.obj.message['from_id']]['words_game'][2] and not \
                id_d[event.obj.message['from_id']]['help'][8] and wait_answ and \
                event.obj.message['peer_id'] == 2000000001:

            print('добавляю')
            wait_answ = False

            if 'добавить' in event.obj.message['text'].lower():

                Words.WordsGame().add_word(gl_add_word[1])

                text = f"Слово {gl_add_word[1]} было добавлено в словарь. Благодарим за Ваше предложение\n"\
                    f"Слово {gl_add_word[1]} - Ваш ход, и считается использованным"

                print(id_d[event.obj.message['from_id']]['words'].keys())
                if gl_add_word[1][0] not in id_d[event.obj.message['from_id']]['words'].keys():
                    id_d[event.obj.message['from_id']]['words'][gl_add_word[1][0]] = []

                id_d[event.obj.message['from_id']]['words'][gl_add_word[1][0]].append(gl_add_word[1])
                print(id_d[event.obj.message['from_id']]['words'])

            else:
                text = f"Слово {gl_add_word[1]} не было добавлено в словарь. Но благодарим за Ваше предложение"

            vk.messages.send(peer_ids=['2000000001', gl_add_word[0]],
                             message=text,
                             random_id=random.randint(0, 2 ** 64))

            # удаляем добавленное слово из списка
            # под ключом-id пользователя, предложившего само слово
            words_add_d[gl_add_word[0]].pop(0)

            if not words_add_d[gl_add_word[0]]:   # проверка, предлагал ли пользователь еще какие-то слова
                print('1111', words_add_d)
                # удаляем id пользователя, если больше нет предлагаемых слов
                # из словаря с ключами + списками предложений
                words_add_d.pop(gl_add_word[0])
                print('1113', words_add_d)

            id_d[gl_add_word[0]]['add_word'] = ''   # очищаем у id переменную - предлагаемое слово

            print("id_d[gl_add_word[0]]['add_word'] = ", id_d[gl_add_word[0]]['add_word'])
            # words_add_d[gl_add_word[0]].pop(0)

            gl_add_word = ['', '']   # очищаем глобальную переменную с id пользователя и предлагаемым им словом

            print("gl_add_word =", gl_add_word)
            print("words_add_d = ", words_add_d)

            if words_add_d.keys():   # проверка, есть ли еще id пользователей с предложениями слов

                id = random.choice(id_add_sp)
                gl_add_word[0], gl_add_word[1] = id, words_add_d[id][0]
                id_d[gl_add_word[0]]['add_word'] = gl_add_word[1]

                text = f'''Пользователь {gl_add_word[0]} хочет добавить слово \n
                💡{gl_add_word[1]}💡'''
                '''Добавить / Не добавлять'''

                wait_answ = True
                vk.messages.send(peer_id='2000000001',
                                 message=text,
                                 keyboard=open('keyboard\keyboard_add_not.json', 'r',
                                               encoding='UTF-8').read(),
                                 random_id=random.randint(0, 2 ** 64))
            else:

                text = '''На данный момент больше предложений не поступало'''
                wait_answ = False
                vk.messages.send(peer_id='2000000001',
                                 message=text,
                                 keyboard=open('keyboard\keyboard_add_not.json', 'r',
                                               encoding='UTF-8').read(),
                                 random_id=random.randint(0, 2 ** 64))

        else:
            if event.type == VkBotEventType.MESSAGE_NEW and \
                    event.obj.message['peer_id'] == 2000000001 and not wait_answ:
                text = 'Пока нет слов-предложений для добаления в БД'

                vk.messages.send(peer_id='2000000001',
                                 message=text,
                                 keyboard=open('keyboard\keyboard_add_not.json', 'r',
                                               encoding='UTF-8').read(),
                                 random_id=random.randint(0, 2 ** 64))
            if event.type == VkBotEventType.MESSAGE_NEW and \
                    event.obj.message['peer_id'] == 2000000001 and wait_answ and \
                ('добавить' in event.obj.message['text'].lower() or \
                 'не добавлять' in event.obj.message['text'].lower()):

                text = f'''Пользователь {gl_add_word[0]} хочет добавить слово \n💡{gl_add_word[1]}💡'''
                '''Добавить / Не добавлять'''

                vk.messages.send(peer_id='2000000001',
                                 message=text,
                                 keyboard=open('keyboard\keyboard_add_not.json','r',
                                               encoding='UTF-8').read(),
                                 random_id=random.randint(0, 2 ** 64))

            if event.type == VkBotEventType.MESSAGE_NEW and \
                        id_d[event.obj.message['from_id']]['help'][0]:   # запрос на ввод фразы, запускающей бот

                    text = "Для начала работы напишите 'Начать'"

                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     keyboard=open('keyboard\keyboard_start.json',
                                                   'r',
                                                   encoding='UTF-8').read(),
                                     random_id=random.randint(0, 2 ** 64))
            elif event.type == VkBotEventType.MESSAGE_NEW and \
                        id_d[event.obj.message['from_id']]['help'][1]:   # запрос на выбор одного из доступных навыков

                    text = "Выберите один из навыков:\n" \
                                   "✅ Игры\n" \
                                   "✅ Погода\n" \
                                   "✅ Время\n" \
                                   "✅ Карты\n" \
                                   "✅ Удача\n"

                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     keyboard=open('keyboard\keyboard_menu.json',
                                                   'r',
                                                   encoding='UTF-8').read(),
                                     random_id=random.randint(0, 2 ** 64))

            elif event.type == VkBotEventType.MESSAGE_NEW and \
                        id_d[event.obj.message['from_id']]['help'][2]:   # запрос на выбор одной из доступных игр

                    text = "Выберите игру:\n" \
                           "○ Камень-ножницы-бумага\n" \
                           "○ Угадай число\n" \
                           "○ Слова\n" \
                           "○ быки - коровы\n"

                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     keyboard=open('keyboard\keyboard_games.json', 'r',
                                                   encoding='UTF-8').read(),
                                     random_id=random.randint(0, 2 ** 64))

            elif event.type == VkBotEventType.MESSAGE_NEW and \
                        id_d[event.obj.message['from_id']]['help'][3]:   # подсказка о выборе игрока, делающего первый ход(игра "угадай число")

                    text = "Выберите, кто загадывает число: Я или ВЫ?\n" \
                           "Напишите СТОП - если хотите завершить игру\n"

                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     keyboard=open('keyboard\keyboard_i_y_stop.json', 'r',
                                         encoding='UTF-8').read(),
                                     random_id=random.randint(0, 2 ** 64))

            elif event.type == VkBotEventType.MESSAGE_NEW and \
                        id_d[event.obj.message['from_id']]['help'][4]:   # опрос, загадал ли игрок число(игра "угадай число")

                    text = "Вы загадали число? ДА / НЕТ"

                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     keyboard=open('keyboard\keyboard_y_n.json', 'r',
                                                   encoding='UTF-8').read(),
                                     random_id=random.randint(0, 2 ** 64))

            elif event.type == VkBotEventType.MESSAGE_NEW and \
                        id_d[event.obj.message['from_id']]['help'][5]:   # подсказка о вводе ответа "больше", "меньше" или "равно"
                    text = "Введите БОЛЬШЕ, МЕНЬШЕ или РАВНО"

                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     keyboard=open('keyboard\keyboard_b_m_r.json', 'r',
                                                   encoding='UTF-8').read(),
                                     random_id=random.randint(0, 2 ** 64))

            elif event.type == VkBotEventType.MESSAGE_NEW and \
                        id_d[event.obj.message['from_id']]['help'][6]:   # подсказка на ввод максимально возможного загаданного ботом числа

                    text = "Введите максимальное число, которое мне можно загадать\n" \
                           "Минимальное число - 0"

                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     keyboard=open('keyboard\keyboard_stop.json','r',
                                                   encoding='UTF-8').read(),
                                     random_id=random.randint(0, 2 ** 64))

            elif event.type == VkBotEventType.MESSAGE_NEW and \
                        id_d[event.obj.message['from_id']]['help'][7]:   # подсказка о вводе угадываемого пользователем числа

                    text = "Введите число, которое думаете, я загадал\n"

                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     keyboard=open('keyboard\keyboard_stop.json','r',
                                                   encoding='UTF-8').read(),
                                     random_id=random.randint(0, 2 ** 64))

            elif event.type == VkBotEventType.MESSAGE_NEW and \
                        id_d[event.obj.message['from_id']]['help'][8]:   # подсказка о вводе ответа "перезапустить"\"не перезапускать"

                    text = "Напишите мне -  ПЕРЕЗАПУСТИТЬ игру / НЕ ПЕРЕЗАПУСКАТЬ"

                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     keyboard=open('keyboard\keyboard_start_notstart.json', 'r',
                                         encoding='UTF-8').read(),
                                     random_id=random.randint(0, 2 ** 64))

            elif event.type == VkBotEventType.MESSAGE_NEW and \
                        id_d[event.obj.message['from_id']]['help'][9]:   # подсказка на ввод названия города

                    text = "Введите название города, данные для которого Вы хотели бы получить. Для выхода напишите СТОП"

                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     keyboard=open('keyboard\keyboard_stop.json', 'r',
                                         encoding='UTF-8').read(),
                                     random_id=random.randint(0, 2 ** 64))

            elif event.type == VkBotEventType.MESSAGE_NEW and \
                        id_d[event.obj.message['from_id']]['help'][10]:  # подсказка-уточнение названия искомого города

                    text = f'''Вы хотите получить данные о городе {id_d[event.obj.message['from_id']]['lg_lt_city'][2]}?\n Введите ДА или НЕТ'''

                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     keyboard=open('keyboard\keyboard_y_n.json', 'r',
                                         encoding='UTF-8').read(),
                                     random_id=random.randint(0, 2 ** 64))

            elif event.type == VkBotEventType.MESSAGE_NEW and \
                        id_d[event.obj.message['from_id']]['help'][11]:  # подсказка о выборе пользователем временного промежутка

                    text = "Прогноз погоды на:\n" \
                           "○ Данный момент\n"\
                           "○ Определенное время"

                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     keyboard=open('keyboard\keyboard_now_parts.json', 'r',
                                                   encoding='UTF-8').read(),
                                     random_id=random.randint(0, 2 ** 64))

            elif event.type == VkBotEventType.MESSAGE_NEW and \
                        id_d[event.obj.message['from_id']]['help'][12]:  # подсказка о выборе пользователем временного промежутка(режим "определенное время")

                    text = "Вы можете получить прогноз погоды на:\n" \
                        f"○ {id_d[event.obj.message['from_id']]['ct_parts'][0]}\n" \
                        f"○ {id_d[event.obj.message['from_id']]['ct_parts'][1]}\n"

                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=text,
                                     random_id=random.randint(0, 2 ** 64))

            elif event.type == VkBotEventType.MESSAGE_NEW and \
                        id_d[event.obj.message['from_id']]['help'][13]:   # подсказка-запрос выбора режима игры(игра «Слова»)

                text = "Выберите режим игры:\n" \
                       "○ На все буквы\n" \
                       "○ На одну букву"

                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 keyboard=open('keyboard\keyboard_all_one.json','r',
                                               encoding='UTF-8').read(),
                                 random_id=random.randint(0, 2 ** 64))

            elif event.type == VkBotEventType.MESSAGE_NEW and \
                        id_d[event.obj.message['from_id']]['help'][14]:   # подсказка-запрос о вводе буквы, на которую должны начинаться слова в режиме «на одну  букву»(игра «Слова»)

                text = 'Назовите букву, на которую будут начинаться слова(кроме ъ, ь, ы)'

                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 keyboard=open('keyboard\keyboard_stop.json','r',
                                               encoding='UTF-8').read(),
                                 random_id=random.randint(0, 2 ** 64))

            elif event.type == VkBotEventType.MESSAGE_NEW and \
                        id_d[event.obj.message['from_id']]['help'][15]:    # подсказка, кто начинает игру(игра «Слова»)

                text = "Выберите, кто начинает: Я или ВЫ?\n" \
                       "Напишите СТОП - если хотите завершить игру\n"

                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 keyboard=open('keyboard\keyboard_i_y_stop.json', 'r',
                                     encoding='UTF-8').read(),
                                 random_id=random.randint(0, 2 ** 64))

            elif event.type == VkBotEventType.MESSAGE_NEW and \
                        id_d[event.obj.message['from_id']]['help'][16]:   # подсказка, о вводе первого слова на нужную букву(игра «Слова»)

                if id_d[event.obj.message['from_id']]['one_let']:
                    text = f"Назовите слово на букву {id_d[event.obj.message['from_id']]['one_let']}"
                else:
                    text = "Назовите слово на любую букву\n"

                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 keyboard=open('keyboard\keyboard_stop.json','r',
                                               encoding='UTF-8').read(),
                                 random_id=random.randint(0, 2 ** 64))

            elif event.type == VkBotEventType.MESSAGE_NEW and \
                        id_d[event.obj.message['from_id']]['help'][17]:   # подсказка, о вводе слова на нужную букву(игра «Слова»)

                if id_d[event.obj.message['from_id']]['one_let']:
                    text = f"Назовите слово на букву {id_d[event.obj.message['from_id']]['one_let']}"
                else:
                    text = f"Назовите слово на букву {id_d[event.obj.message['from_id']]['all_last_let']}"

                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 keyboard=open('keyboard\keyboard_stop.json','r',
                                               encoding='UTF-8').read(),
                                 random_id=random.randint(0, 2 ** 64))

            elif event.type == VkBotEventType.MESSAGE_NEW and \
                        id_d[event.obj.message['from_id']]['help'][18]:   # подсказка-опрос, о начале игры(игра «Слова»)

                text = "Для продолжения напишите - ДА\n" \
                       "Для завершения игры - НЕТ"

                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 keyboard=open('keyboard\keyboard_y_n.json','r',
                                               encoding='UTF-8').read(),
                                 random_id=random.randint(0, 2 ** 64))

            elif event.type == VkBotEventType.MESSAGE_NEW and \
                        id_d[event.obj.message['from_id']]['help'][19]:   # подсказка-опрос, хочет ли пользователь предложить добавить слово и БД или нет(игра «Слова»)

                text = "Введите «Добавить слово», если хотите предложить это сделать»"

                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 keyboard=open('keyboard\keyboard_y_n.json','r',
                                               encoding='UTF-8').read(),
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
