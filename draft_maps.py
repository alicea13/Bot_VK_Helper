import os
import sys
import requests


class Cities:
    def __init__(self, city, skill_name, street='', house=''):
        self.city = city
        self.skill_name = skill_name

        self.street = street
        self.house = house

        # out = self.search(self.city)
        # print("Cities.search ", out)

    def search(self, toponym, id_city='', id_house=''):
        if toponym:

            geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

            # print(',+'.join(toponym.split()))

            geocoder_params = {
                "apikey": "a954d541-8a0c-4fef-9924-6be4d4bf3b12",

                # "geocode": ',+'.join(toponym.split()),

                "geocode": toponym,
                "format": "json"}

            response = requests.get(geocoder_api_server, params=geocoder_params)

            json_response = response.json()

            # print(json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point'])

            if json_response['response']["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]['found'] != '0':
                kind_area = json_response["response"]["GeoObjectCollection"][
                    "featureMember"][0]["GeoObject"]["metaDataProperty"][
                    "GeocoderMetaData"]['Address']['Components'][-1]["kind"]

                if self.skill_name == 'weather':
                    if kind_area == 'province' or kind_area == 'locality':

                        toponym = json_response["response"]["GeoObjectCollection"][
                            "featureMember"][0]["GeoObject"]

                        city = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
                              "GeocoderMetaData"]['Address']['Components'][-1][
                              'name']

                        toponym_coodrinates = toponym["Point"]["pos"]
                        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

                        return toponym_longitude, toponym_lattitude, city
                    else:
                        text = "Извините, я не знаю такого города. Может, Вы допустили ошибку?\n" \
                               "Попробуйте ввести название города еще раз"
                    return text

                if self.skill_name == 'maps':
                    if self.city and not self.street and not self.house:
                        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]

                        # print(toponym)
                        city = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
                                "GeocoderMetaData"]['Address']['Components'][2]['name']
                        print(city)

                        toponym_coodrinates = toponym["Point"]["pos"]
                        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(
                            " ")

                        return toponym_longitude, toponym_lattitude, city
                    if self.city and self.street and not self.house:
                        street = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
                                "GeocoderMetaData"]['Address']['Components'][4]['name']
                        print(street)

                        toponym_coodrinates = toponym["Point"]["pos"]
                        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

                        return toponym_longitude, toponym_lattitude, id_city, street
                    if self.house:
                        house = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
                                "GeocoderMetaData"]['Address']['Components'][5]['name']
                        print(house)
                        print(toponym)
                        toponym_coodrinates = toponym["Point"]["pos"]
                        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

                        return toponym_longitude, toponym_lattitude, id_city, id_street, house


            else:
                text = "Извините, я не знаю такого города. Может, Вы допустили ошибку?\n"\
                        "Попробуйте ввести название города еще раз"
                return text

        else:
            text = "Извините, я не знаю такого города. Может, Вы допустили ошибку?\n"\
                   "Попробуйте ввести название города еще раз"
            return text


def request(coord_x, coord_y, toponym, delta, user_id, zoom, l_param):
    # map_request = "http://static-maps.yandex.ru/1.x/?"
    map_request = "https://static-maps.yandex.ru/1.x/"

    map_params = {
        "ll": ",".join([coord_x, coord_y]),
        "spn": ",".join([str(delta), str(delta)]),
        "l": str(l_param),
        'z': zoom,
        'controls': ['searchControl'],
        'searchControlProvider': 'yandex#search'}

    response = requests.get(map_request, params=map_params)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = f"{user_id}.png"

    filename = 'maps_photo/' + map_file
    if not os.path.exists(os.path.dirname(filename)):
        dir_name = os.path.dirname(filename)
        os.makedirs(dir_name)

    with open(filename, "wb") as file:
        file.write(response.content)
    return map_file


city = Cities('москва', 'weather', 1, 1)
long, lat, c, st = city.search('москва')
# print(long, lat)

map = request(long, lat, c, 0.01, 1, 17, 'map')
