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
                                                  'help': [True, False]}

        if event.type == VkBotEventType.MESSAGE_NEW and \
                event.obj.message['text'].lower() == 'начать' \
                and not id_d[event.obj.message['from_id']]['flag']:

            id_d[event.obj.message['from_id']]['flag'] = True

            id_d[event.obj.message['from_id']]['help'][0] = False
            id_d[event.obj.message['from_id']]['help'][1] = True

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




if __name__ == '__main__':
    main()