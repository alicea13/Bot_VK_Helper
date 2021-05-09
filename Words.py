# import requests, random
import sqlite3, random
from addition import data_words_addition


conn = sqlite3.connect('VK_words_alphabet.db')
cursor = conn.cursor()

#   добавления букв алфавита в таблицу alphabet
'''
cursor.execute("""CREATE TABLE IF NOT EXISTS alphabet(
                id INT PRIMARY KEY,
                letter TEXT);""")
conn.commit()

c = 1
for let in data_words_addition.words_add.keys():
    values = (c, let)
    cursor.execute('INSERT INTO alphabet(id, letter) VALUES(?, ?);', values)
    conn.commit()
    c += 1
'''
#   создание 29 таблиц(название - буква алфавита) со словами на букву заглавия
'''
for let in list(data_words_addition.words_add.keys()):
    cursor = conn.cursor()
    name = let
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {name}(
                        id INT PRIMARY KEY,
                        first_letter TEXT,
                        word TEXT,
                        used TEXT,
                        FOREIGN KEY (first_letter) REFERENCES VK_words_alphabet(letter));""")
    conn.commit()
    count = 1
    for word in data_words_addition.words_add[let]:
        values = (count, name, word, False)
        cursor  .execute(f"""INSERT INTO {name}(id, first_letter, word, used)
                        VALUES(?, ?, ?, ?);""", values)
        count += 1
        conn.commit()
'''

###


class WordsGame:
    def find_word(self, except_w={}, f_lett='', one=False, word=''):
        # if not one:
        #     f_lett = word[-1]
        print(except_w, f_lett, one, word)
        if except_w:
            words = [i[0] for i in list(cursor.execute(f'''SELECT word FROM {f_lett}''').fetchall())]
            print(words)
            # if one:
            #     words.remove(word)
            if f_lett in except_w.keys():   # проверка назывались слова на эту букву
                for w in except_w[f_lett]:   # проходим по словарю названых слов пользователя
                    if w in words:
                        words.remove(w)
            if words:   # если посде удаления остались слова
                word_out = random.choice(words)   # рандомно-выбранное слово
            else:
                return True, open('keyboard\keyboard_start_notstart.json', 'r', encoding='UTF-8').read(), \
                       f'''Я больше не знаю слов на букву {f_lett}\n \ 
                               Вы выиграли\n \ 
                               Напишите мне -  ПЕРЕЗАПУСТИТЬ игру / НЕ ПЕРЕЗАПУСКАТЬ'''
            print(word_out)
            print('ok')
        else:
            print(word)
            words = self.first_move(f_lett)
            if one:
                words.remove(word)
            print(words)
            word_out = random.choice(words)
            print(word_out)

        if one:
            return False, open('keyboard\keyboard_stop.json', 'r', encoding='UTF-8').read(), (word_out, f_lett)
        else:
            if word_out[-1] in 'ъьы':
                return False, open('keyboard\keyboard_stop.json', 'r', encoding='UTF-8').read(), (word_out, word_out[-2])
            return False, open('keyboard\keyboard_stop.json', 'r', encoding='UTF-8').read(), (word_out, word_out[-1])

    def first_move(self, first_l):
        if not first_l:
            first_l = random.choice('абвгдеёжзийклмнопрстуфхцчшщэюя')
            print(first_l)

        words = [i[0] for i in list(cursor.execute(f'''SELECT word FROM {first_l}''').fetchall())]

        print(len(words))
        return words

    def check_word(self, word, except_w, f_let=''):
        print('95', word, except_w, f_let)
        if word[0] not in 'ъыь':
            # проверка есть ли слово в БД
            check = cursor.execute(f'''SELECT id FROM {word[0]} WHERE word = ?''', (word,)).fetchall()
            if check:

                if f_let:   # задана первая буква(режим "на одну букву")
                    if except_w:
                        return self.find_word(except_w, f_let, True, word)
                    return self.find_word({}, f_let, True, word)
                else:
                    if except_w:
                        if word[-1] in 'ъьы':
                            return self.find_word(except_w, word[-2], f_let, word)
                        else:
                            return self.find_word(except_w, word[-1], f_let, word)
                    else:
                        if word[-1] in 'ъьы':
                            return self.find_word({}, word[-2], f_let, word)
                        else:
                            return self.find_word({}, word[-1], f_let, word)

                '''if word[-1] in 'ъьы' and except_w:
                        return self.find_word(except_w, word[-2])
                   return self.find_word(f_lett=word[-1], )'''

            else:
                return False, open('keyboard\keyboard_stop.json', 'r', encoding='UTF-8').read(), \
                       "Введенное Вами слово мне не знакомо.\n" \
                       " Попробуйте ввести другое"
        else:
            return False, open('keyboard\keyboard_stop.json', 'r', encoding='UTF-8').read(), \
                       "Введенное Вами слово мне не знакомо.\n" \
                       " Попробуйте ввести другое"
