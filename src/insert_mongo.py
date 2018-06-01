from pymongo import MongoClient
from tqdm import tqdm
import oop_work_with_api
from datetime import datetime
import requests
import mimetypes
import logging
import gridfs

logger = logging.getLogger(__name__)

client = MongoClient('mongodb://rbogdanov:RomA48917050@localhost:27017/')
client2 = MongoClient('mongodb://rbogdanov:RomA48917050@localhost:27017/Kinohod')
dbb = client2['Kinohod']
db = client['Kinohod_files']
client_f = MongoClient('localhost:27017',
                       username='rbogdanov',
                       password='RomA48917050',
                       authSource='Kinohod_files',
                       authMechanism='SCRAM-SHA-1')
fs = gridfs.GridFS(client_f['Kinohod_files'])


def fill_halls(j_file):
    for hall in tqdm(j_file):
        cursor = dbb.halls.find({'_id': hall.get('id')})
        if cursor.count() == 0:
            dbb.halls.update({
                '_id': hall.get('id')
            }, hall, upsert=True)
            logger.debug('Hall with id - {}, was added to db'.format(hall.get('id')))


def fill_cinemas(j_file):
    for cinema in tqdm(j_file):
        cursor = dbb.cinemas.find({'_id': cinema.get('id')})
        if cursor.count() == 0:
            dbb.cinemas.update({
                '_id': cinema.get('id')
            }, cinema, upsert=True)
            logger.debug('Cinema with id - {}, was added to db'.format(cinema.get('id')))


def fill_networks(j_file):
    for network in tqdm(j_file):
        cursor = dbb.networks.find({'_id': network.get('id')})
        if cursor.count() == 0:
            dbb.networks.update({
                '_id': network.get('id')
            }, network, upsert=True)
            logger.debug('Network with id - {}, was added to db'.format(network.get('id')))


def fill_movies(j_file):
    k = 0
    for movie in tqdm(j_file):
        k += 1
        if isinstance(movie['id'], str):
            movie['id'] = int(movie.get('id'))
        cursor = dbb.movies.find({'_id': movie.get('id')})
        if cursor.count() == 0:
            if movie.get('premiereDateWorld'):
                if isinstance(movie.get('premiereDateWorld'), str):
                    movie['premiereDateWorld'] = datetime.strptime(movie.get('premiereDateWorld'), '%Y-%m-%d')
            if movie.get('premiereDateRussia'):
                if isinstance(movie.get('premiereDateRussia'), str):
                    movie['premiereDateRussia'] = datetime.strptime(movie.get('premiereDateRussia'), '%Y-%m-%d')
            dbb.movies.update({'_id': movie.get('id')}, movie, upsert=True)
            if k % 50 == 0:
                logger.debug("Movie {} was added to db".format(movie.get('title')))
            if movie.get('posterLandscape').get('name'):
                insert_poster(movie, 'posterLandscape')
            if movie.get('poster').get('name'):
                insert_poster(movie, 'poster')
            if movie.get('images'):
                i = -1
                for image in movie.get('images'):
                    i += 1
                    if image.get('name'):
                        filename = image.get('name')
                        image_url = get_image_url(image)
                        im_id = add_image(image_url, filename)
                        dbb.movies.update({'_id': movie.get('id')},
                                         {'$set':
                                              {"images.{0}.file_id".format(str(i)): im_id
                                               }
                                          })
            if movie.get('trailers'):
                i = -1
                for element in movie.get('trailers'):
                    i += 1
                    if element.get('preview').get('name'):
                        filename = element.get('preview').get('name')
                        image_url = get_image_url(element.get('preview'))
                        im_id = add_image(image_url, filename)
                        dbb.movies.update({"_id": movie.get('id')},
                                         {"$set":
                                              {'trailers.{0}.preview.file_id'.format(str(i)): im_id
                                               }
                                          })
                    if element.get('source').get('filename'):
                        filename = element.get('source').get('filename')
                        image_url = get_image_url(element.get('source'), 'filename')
                        im_id = add_image(image_url, filename)
                        dbb.movies.update({"_id": movie.get('id')},
                                         {"$set":
                                              {"trailers.{0}.source.file_id".format(str(i)): im_id
                                               }
                                          })
                    if element.get('videos'):
                        j = -1
                        for video in element.get('videos'):
                            j += 1
                            if video.get('filename'):
                                filename = video.get('filename')
                                image_url = get_image_url(video, 'filename')
                                im_id = add_image(image_url, filename)
                                dbb.movies.update({"_id": movie.get('id')},
                                                 {"$set":
                                                      {"trailers.{0}.videos.{1}.file_id".format(str(i), str(j)): im_id
                                                       }
                                                  })


def insert_poster(movie, key_word):
    filename = movie.get(key_word)
    image_url = get_image_url(movie.get(key_word))
    f_id = add_image(image_url, filename)
    dbb.movies.update({"_id": movie.get('id')},
                     {"$set":
                          {key_word + ".file_id": f_id}
                      })


def add_image(image_url, filename):
    gridfs_filename = filename
    mime_type = mimetypes.guess_type(image_url)[0]
    r = requests.get(image_url, stream=True)
    kd = fs.put(r.raw, contentType=mime_type, filename=gridfs_filename)
    return kd


def get_image_url(ddict, field='name'):
    image_url = 'http://{HOST}/p/1000x300/{ab}/{cd}/{uuid}.{ext}'.format(HOST='www.kinohod.ru',
                                                                         ab=ddict.get(field)[:2],
                                                                         cd=ddict.get(field)[2:4],
                                                                         uuid=ddict.get(field).split('.')[0],
                                                                         ext=ddict.get(field).split('.')[1])
    return image_url


def fill_ceanses(j_file):
    i = 0
    for seance in tqdm(j_file):
        cursor = dbb.seanses.find({'_id': seance.get('id')})
        if cursor.count() == 0:
            if isinstance(seance['id'], str):
                seance['id'] = int(seance.get('id'))
            seance['date'] = datetime.strptime(seance['date'], '%Y-%m-%d'),
            seance['time'] = datetime.strptime(seance['time'], '%H:%M'),
            seance['startTime'] = datetime.strptime(seance['startTime'] + '00', '%Y-%m-%d %H:%M:%S%z')
            dbb.seanses.update({
                '_id': seance.get('id')
            }, seance, upsert=True)
            i += 1
    logger.debug("{} new ceanses was added to db".format(i))


def fill_distributors(j_file):
    for distributor in tqdm(j_file):
        cursor = dbb.distributors.find({'_id': distributor.get('id')})
        if cursor.count() == 0:
            dbb.distributors.update({
                '_id': distributor.get('id')
            }, distributor, upsert=True)
            logger.debug("Distributor with id - {} was added to db".format(distributor.get('id')))


def fill_cities(j_file):
    for city in tqdm(j_file):
        cursor = dbb.cities.find({'_id': city.get('id')})
        if cursor.count() == 0:
            dbb.cities.update({
                '_id': city.get('id')
            }, city, upsert=True)
            logger.debug("City with id - {} was added to db".format(city.get('id')))


def fill_subways(j_file):
    for subway_station in tqdm(j_file):
        cursor = dbb.subways.find({'_id': subway_station.get('id')})
        if cursor.count() == 0:
            dbb.subways.update({
                '_id': subway_station.get('id')
            }, subway_station, upsert=True)
            logger.debug("Subway with id - {} was added to db".format(subway_station.get('id')))



def fill_genres(j_file):
    for genre in j_file:
        cursor = dbb.genres.find({'_id': genre.get('id')})
        if cursor.count() == 0:
            dbb.genres.update({
                '_id': genre.get('id')
            }, genre, upsert=True)
            logger.debug("Genre with id - {} was added to db".format(genre.get('id')))



if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(module)s %(message)s",
        level=10)

    a = oop_work_with_api.ApiKinohod('https://api.kinohod.ru/api/data/2/5982bb5a-1d76-31f8-abd5-c4253474ecf3/')
    fill_halls(a.get_json(a.halls))
    fill_cinemas(a.get_json(a.cinemas))
    fill_movies(a.get_json(a.movies))
    fill_ceanses(a.get_json(a.seances))
    fill_networks(a.get_json(a.networks))
    fill_distributors(a.get_json(a.distributors))
    fill_cities(a.get_json(a.cities))
    fill_genres(a.get_json(a.genres))
    fill_subways(a.get_json(a.genres))
