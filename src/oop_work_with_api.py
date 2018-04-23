import requests
import pandas as pd



class ApiKinohod():
    def __init__(self, api_key):
        self.HTTP_OK = 200
        self.api_key = api_key
        self.distributors = 'distributors.json'
        self.cities = 'cities.json'
        self.networks = 'networks.json'
        self.halls = 'halls.json'
        self.subways = 'subways.json'
        self.genres = 'genres.json'
        self.languages = 'languages.json'
        self.accept = {"Accept-Encoding": "json"}

    def get_json(self, method):
        link = self.api_key + method
        movies_soon = requests.get(link, headers=self.accept)
        if movies_soon.status_code == self.HTTP_OK:
            print(movies_soon.status_code)
            movies_soon_json = movies_soon.json()
            return pd.DataFrame(movies_soon_json)
        else:
            print('error')


if __name__ == '__main__':
    a = ApiKinohod('https://api.kinohod.ru/api/data/2/5982bb5a-1d76-31f8-abd5-c4253474ecf3/')
    df = a.get_json(a.languages)
    print(df.head(15))