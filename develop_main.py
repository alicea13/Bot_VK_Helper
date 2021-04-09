import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random

import addition.data_doc_addition

vk_session = vk_api.VkApi(
    token='ffcaa658692c13d6c1bf5fe7946572169e6c4fb1c76ca4e8aef0fb4ddf60ae95e97210da8d6b677df6fb6')
longpoll = VkBotLongPoll(vk_session, '199196587')

flag = False
flag_play = False

id_d = dict()

print('start')


def main():
    global flag, flag_play, id_d
    for event in longpoll.listen():

        vk = vk_session.get_api()
        if event.type == VkBotEventType.MESSAGE_NEW and \
                event.obj.message['from_id'] not in id_d.keys():
            id_d[event.obj.message['from_id']] = {'flag': False,
                                                  'flag_play': False,
                                                  'number_game': False,
                                                  'help': [True, False, False,
                                                           False]}

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
            event.obj.message['text'].lower() and \
                id_d[event.obj.message['from_id']]['flag']:   # обработка запуска навыка "игры"

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
                             random_id=random.randint(0, 2 ** 64))

        else:
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
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()