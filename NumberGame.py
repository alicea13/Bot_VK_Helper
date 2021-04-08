import random


class NumberGamePolz:
    def __init__(self, nb_gm_fl, nb_gm_plz, h_6):
        self.maxim = 1000
        self.minim = 0

        self.number_game_fl = nb_gm_fl
        self.number_game_plz = nb_gm_plz
        self.help6 = h_6

        self.middle = (self.minim + self.maxim) // 2
        self.numbers = [i for i in range(1000)]

    def numb_game_plz_func(self, answ):
        if answ == "меньше" or answ == "больше":
            if answ == "меньше":
                self.minim = self.middle

            else:
                self.maxim = self.middle

            self.middle = (self.minim + self.maxim) // 2

            if self.minim < self.maxim - 1:
                self.help6 = True
                return self.help6, False, open('keyboard\keyboard_b_m_r.json', 'r',
                                               encoding='UTF-8').read(),\
                       f"Число {self.numbers[self.middle]} БОЛЬШЕ, МЕНЬШЕ " \
                       f"или РАВНО вашему числу?"
            else:
                self.help6 = False
                return self.help6, True, open('keyboard\keyboard_start_notstart.json', 'r', encoding='UTF-8').read(),\
                       "Должно быть, Вы ошиблись. Такого числа нет в " \
                       "диапазоне от 1 до 1000\n" \
                       "Напишите мне -  ПЕРЕЗАПУСТИТЬ игру / НЕ ПЕРЕЗАПУСКАТЬ"

        elif answ == "равно":
            self.help6 = False
            return self.help6, True, open('keyboard\keyboard_start_notstart.json', 'r', encoding='UTF-8').read(),\
                   f"Ура! У меня получилось !\n " \
                   f"Ваше число : {self.numbers[self.middle]}\n" \
                   "Напишите мне -  ПЕРЕЗАПУСТИТЬ игру / НЕ ПЕРЕЗАПУСКАТЬ"
        self.help6 = False
        return self.help6, True, open('keyboard\keyboard_start_notstart.json', 'r', encoding='UTF-8').read(), \
               "Должно быть, Вы ошиблись. Такого числа нет в " \
               "диапазоне от 1 до 1000\n" \
               "Напишите мне -  ПЕРЕЗАПУСТИТЬ игру / НЕ ПЕРЕЗАПУСКАТЬ"

    def number_game_st(self):
        return f"Число {self.numbers[self.middle]} БОЛЬШЕ, МЕНЬШЕ " \
               f"или РАВНО вашему числу?", open('keyboard\keyboard_b_m_r.json', 'r', encoding='UTF-8').read()

