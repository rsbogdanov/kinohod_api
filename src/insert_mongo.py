from pymongo import MongoClient
from tqdm import tqdm
import oop_work_with_api
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


client = MongoClient('mongodb://localhost:27017/')
db = client['Kinohod']


def fill_halls(j_file):
    for hall in tqdm(j_file):
        db.halls.update({
            '_id': hall.get('id')
        }, hall, upsert=True)

def fill_cinemas(j_file):
    for cinema in tqdm(j_file[:1000]):
        db.cinemas.update({
            '_id': cinema.get('id')
        }, cinema, upsert=True)

def fill_networks(j_file):
    for network in tqdm(j_file):
        db.networks.update({
            '_id': network.get('id')
        }, network, upsert=True)

def fill_movies(j_file):
    for movie in tqdm(j_file):
        if isinstance(movie['id'], str):
            movie['id'] = int(movie.get('id'))
        if movie.get('premiereDateWorld'):
            movie['premiereDateWorld'] = datetime.strptime(movie.get('premiereDateWorld'), '%Y-%m-%d')
        if movie.get('premiereDateRussia'):
            movie['premiereDateRussia'] = datetime.strptime(movie.get('premiereDateRussia'), '%Y-%m-%d')
        db.movies.update({
            '_id': movie.get('id')
        }, movie, upsert=True)

def fill_ceanses(j_file):
    for seance in tqdm(j_file):
        if isinstance(seance['id'], str):
            seance['id'] = int(seance.get('id'))
        seance['date'] = datetime.strptime(seance['date'], '%Y-%m-%d'),
        seance['time'] = datetime.strptime(seance['time'], '%H:%M'),
        seance['startTime'] = datetime.strptime(seance['startTime'] + '00', '%Y-%m-%d %H:%M:%S%z')
        db.seanses.update({
            '_id': seance.get('id')
        }, seance, upsert=True)

def fill_distributors(j_file):
    for distributor in tqdm(j_file):
        db.distributors.update({
            '_id': distributor.get('id')
        }, distributor, upsert=True)

def fill_cities(j_file):
    for city in tqdm(j_file):
        db.cities.update({
            '_id': city.get('id')
        }, city, upsert=True)

def fill_subways(j_file):
    for subway_station in tqdm(j_file):
        db.subways.update({
            '_id': subway_station.get('id')
        }, subway_station, upsert=True)

def fill_genres(j_file):
    for genre in j_file:
        db.genres.update({
            '_id': genre.get('id')
        }, genre, upsert=True)

if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(module)s %(message)s",
        level=10)

    a = oop_work_with_api.ApiKinohod('https://api.kinohod.ru/api/data/2/5982bb5a-1d76-31f8-abd5-c4253474ecf3/')
    #fill_halls(a.get_json(a.halls))
    #fill_cinemas(a.get_json(a.cinemas))
    fill_movies(a.get_json(a.movies))
    fill_ceanses(a.get_json(a.seances))
    #fill_networks(a.get_json(a.networks))
    #fill_networks(a.get_json(a.networks))
    #fill_movies(a.get_json(a.movies))
    # fill_distributors(a.get_json(a.distributors))
    # fill_cities(a.get_json(a.cities))
    # fill_genres(a.get_json(a.genres))
    # fill_subways(a.get_json(a.genres))
    # fill_movies(a.get_json(a.movies))
