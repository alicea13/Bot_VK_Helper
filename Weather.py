import requests
import sys
import datetime
from addition import data_emoji_addition


class Weather:
    def __init__(self, city, now, lat, lon, w_fl):
        self.time = now
        self.city_fl = city
        self.lat = lat
        self.lon = lon
        self.w = w_fl

        self.fact_d = data_emoji_addition.fact_d
        self.condition_d = data_emoji_addition.condition_d
        self.wind_d = data_emoji_addition.wind_d
        self.clock_d = data_emoji_addition.clock_d
        self.daytime_d = data_emoji_addition.daytime_d
        self.sun_d = data_emoji_addition.sun_d
        self.time_d = data_emoji_addition.time_d
        self.season_d = data_emoji_addition.season_d
        self.moon_d = data_emoji_addition.moon_d
        self.parts = data_emoji_addition.parts_d

        self.weather_request = 'https://api.weather.yandex.ru/v2/informers/'

        headers = {'X-Yandex-API-Key': 'fae8e3d1-1c7c-4181-8f93-19da8f9063c3'}
        w_params = {'lat': self.lat,
                    'lon': self.lon,
                    'lang': "ru_RU"}

        self.response = requests.get(self.weather_request, headers=headers, params=w_params)

    def response_d(self, time):
        if self.response:
            json_response = self.response.json()
            if self.w:
                if self.time:
                    fact_w = json_response['fact']

                    text = f"○ Температура воздуха:  {self.fact_d['temp'][0]} {fact_w['temp']}{self.fact_d['temp'][1]}\n" \
                        f"○ Скорость ветра:  {self.fact_d['wind_speed']}  {fact_w['wind_speed']}м/с\n"\
                        f"○ Направление ветра:  {self.wind_d[fact_w['wind_dir']][1]} {self.wind_d[fact_w['wind_dir']][0]}\n"\
                        f"○ Атмосферное давление:  {self.fact_d['pressure_mm']} {fact_w['pressure_mm']}мм рт.ст.\n"\
                        f"○ Влажность воздуха:  {self.fact_d['humidity']} {fact_w['humidity']}%\n"\
                        f"○ Описание погоды:  {self.condition_d[fact_w['condition']][1]} {self.condition_d[fact_w['condition']][0]}\n"
                    return text
                else:
                    if time == '':
                        text = "Вы можете получить прогноз погоды на:\n"\
                               f"○ {self.parts[json_response['forecast']['parts'][0]['part_name']]}\n" \
                               f"○ {self.parts[json_response['forecast']['parts'][1]['part_name']]}\n"
                        return text, [self.parts[json_response['forecast']['parts'][0]['part_name']],
                                      self.parts[json_response['forecast']['parts'][1]['part_name']]]
                    else:
                        text_1 = ''
                        if time == 'Утро':
                            if json_response['forecast']['parts'][0]['part_name'] == 'morning':
                                fact_w = json_response['forecast']['parts'][0]
                                text_1 = f"Прогноз на утро:"
                            elif json_response['forecast']['parts'][1]['part_name'] == 'morning':
                                fact_w = json_response['forecast']['parts'][1]
                                text_1 = f"Прогноз на утро:"
                        elif time == 'День':
                            if json_response['forecast']['parts'][0]['part_name'] == 'day':
                                fact_w = json_response['forecast']['parts'][0]
                                text_1 = f"Прогноз на день:"
                            elif json_response['forecast']['parts'][1]['part_name'] == 'day':
                                fact_w = json_response['forecast']['parts'][1]
                                text_1 = f"Прогноз на день:"
                        elif time == 'Вечер':
                            if json_response['forecast']['parts'][0]['part_name'] == 'evening':
                                fact_w = json_response['forecast']['parts'][1]
                                text_1 = f"Прогноз на вечер:"
                            elif json_response['forecast']['parts'][1]['part_name'] == 'evening':
                                fact_w = json_response['forecast']['parts'][1]
                                text_1 = f"Прогноз на вечер:"
                        elif time == 'Ночь':
                            if json_response['forecast']['parts'][0]['part_name'] == 'night':
                                fact_w = json_response['forecast']['parts'][0]
                                text_1 = f"Прогноз на ночь:"
                            elif json_response['forecast']['parts'][1]['part_name'] == 'night':
                                fact_w = json_response['forecast']['parts'][1]
                                text_1 = f"Прогноз на ночь:"
                        if text_1:

                            text_2 = f"○ Температура воздуха:  {self.fact_d['temp'][0]} {fact_w['temp_avg']}{self.fact_d['temp'][1]}\n" \
                                f"○ Скорость ветра:  {self.fact_d['wind_speed']} {fact_w['wind_speed']}м/с\n" \
                                f"○ Направление ветра:  {self.wind_d[fact_w['wind_dir']][1]} {self.wind_d[fact_w['wind_dir']][0]}\n" \
                                f"○ Атмосферное давление:  {self.fact_d['pressure_mm']} {fact_w['pressure_mm']}мм рт.ст.\n" \
                                f"○ Влажность воздуха:  {self.fact_d['humidity']} {fact_w['humidity']}%\n" \
                                f"○ Описание погоды:  {self.condition_d[fact_w['condition']][1]} {self.condition_d[fact_w['condition']][0]}\n"
                            return text_1, text_2
                        else:
                            text_1 = 'На заданный момент времени мы не можем дать прогноз погоды',
                            text_2 = 'Дайте другой промежуток времени'
                            return text_1, text_2

            else:
                if json_response['fact']['polar']:
                    polar_txt = 'да'
                else:
                    polar_txt = 'нет'
                text = [f"○ Дата:  {self.time_d['date']} {datetime.datetime.now().date()}\n",
                        f"○ Время суток: {self.daytime_d[json_response['fact']['daytime']][1]} {self.daytime_d[json_response['fact']['daytime']][0]}\n",
                        f"○ Порядковый номер недели: #️ {json_response['forecast']['week']}\n",
                        f"○ Время рассвета:  {self.sun_d['sunrise']} {json_response['forecast']['sunrise']}\n",
                        f"○ Время заката:  {self.sun_d['sunset']} {json_response['forecast']['sunset']}\n",
                        f"○ Время года:  {self.season_d[json_response['fact']['season']][0]} {self.season_d[json_response['fact']['season']][1]}\n",
                        f"○ Явление полярной ночи в городе:  {self.time_d['polar']} {polar_txt}\n",
                        f"○ Фаза Луны: {self.moon_d[json_response['forecast']['moon_text']][0]} {self.moon_d[json_response['forecast']['moon_text']][1]}"]
                return ('').join(text)

        else:
            print("Ошибка выполнения запроса:")
            print(self.weather_request)
            print("Http статус:", self.response.status_code, "(", self.response.reason, ")")
            sys.exit(1)