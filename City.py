import requests


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
            print(json_response['response']["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]['found'] == '0')
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