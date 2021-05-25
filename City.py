import requests
import os


class City:
    def __init__(self, city):
        self.city = city

        out = self.search(self.city)
        print("Cities.search ", out)

    def search(self, toponym):
        if toponym:

            geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

            geocoder_params = {
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                "geocode": toponym,
                "format": "json"}

            response = requests.get(geocoder_api_server, params=geocoder_params)

            json_response = response.json()
            if json_response['response']["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]['found'] != '0':
                kind_area = json_response["response"]["GeoObjectCollection"][
                    "featureMember"][0]["GeoObject"]["metaDataProperty"][
                    "GeocoderMetaData"]['Address']['Components'][-1]["kind"]

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
            else:
                text = "Извините, я не знаю такого города. Может, Вы допустили ошибку?\n"\
                       "Попробуйте ввести название города еще раз"
                return text

        else:
            text = "Извините, я не знаю такого города. Может, Вы допустили ошибку?\n"\
                   "Попробуйте ввести название города еще раз"
            return text


# draft

'''def request(coord_x, coord_y, toponym, delta, user_id, zoom, l_param):
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
'''