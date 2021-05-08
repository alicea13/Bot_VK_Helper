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
    def find_word(self, except_w={}, f_lett='', one=False):
        if not f_lett:
            f_lett = random.choice('абвгдеёжзийклмнопрстуфхцчшщэюя')
            print(f_lett)

        words = [i[0] for i in list(cursor.execute(f'''SELECT word FROM {f_lett}''').fetchall())]
        print(except_w)
        print(len(words))
        if f_lett in except_w.keys():
            for w in except_w[f_lett]:
                if w in words:
                    words.remove(w)
        if words:
            word_out = random.choice(words)
        else:
            return True, open('keyboard\keyboard_start_notstart.json', 'r', encoding='UTF-8').read(), \
                   f'''Я больше не знаю слов на букву {f_lett}\n \ 
                           Вы выиграли\n \ 
                           Напишите мне -  ПЕРЕЗАПУСТИТЬ игру / НЕ ПЕРЕЗАПУСКАТЬ'''
        print(word_out)
        # cursor.execute(f'UPDATE {f_lett} SET used = ? WHERE word = ?', ('True', word_out))
        # conn.commit()
        print('ok')
        if one:
            return False, open('keyboard\keyboard_stop.json', 'r', encoding='UTF-8').read(), (word_out, f_lett)
        else:
            if word_out[-1] in 'ъьы':
                return False, open('keyboard\keyboard_stop.json', 'r', encoding='UTF-8').read(), (word_out, word_out[-2])
            return False, open('keyboard\keyboard_stop.json', 'r', encoding='UTF-8').read(), (word_out, word_out[-1])

    def check_word(self, word, except_w=None, f_let=''):
        if word[0] not in 'ъыь':
            check = cursor.execute(f'''SELECT used FROM {word[0]} WHERE word = ?''', (word,)).fetchall()
            if check:
                # cursor.execute(f'UPDATE {word[0]} SET used = ? WHERE word = ?',
                #                ('True', word))
                # conn.commit()
                if f_let:
                    if except_w:
                        return self.find_word(except_w, f_let, True)
                    return self.find_word({}, f_let, True)
                else:
                    if word[-1] in 'ъьы' and except_w:
                        return self.find_word(except_w, word[-2])
                    elif word[-1] in 'ъьы':
                        return self.find_word(word[-2])
                    elif except_w:
                        return self.find_word(except_w, word[-1])
                    return self.find_word(word[-1])
            else:
                return False, open('keyboard\keyboard_stop.json', 'r', encoding='UTF-8').read(), \
                       "Введенное Вами слово мне не знакомо.\n" \
                       " Попробуйте ввести другое"
        else:
            return False, open('keyboard\keyboard_stop.json', 'r', encoding='UTF-8').read(), \
                       "Введенное Вами слово мне не знакомо.\n" \
                       " Попробуйте ввести другое"

