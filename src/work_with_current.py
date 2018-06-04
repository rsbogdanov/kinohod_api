from pymongo import MongoClient
import oop_work_with_api
from datetime import datetime
from tqdm import tqdm
import logging

logger = logging.getLogger(__name__)


client2 = MongoClient('mongodb://rbogdanov:RomA48917050@localhost:27017/Kinohod')
dbb = client2['Kinohod']

def fill_running(j_json):
    for movie in tqdm(j_json):
        if isinstance(movie['id'], str):
            movie['id'] = int(movie.get('id'))
        cursor = dbb.running.find({'_id': movie.get('id')})
        if cursor.count() == 0:
            if movie.get('premiereDateWorld'):
                if isinstance(movie.get('premiereDateWorld'), str):
                    movie['premiereDateWorld'] = datetime.strptime(movie.get('premiereDateWorld'), '%Y-%m-%d')
            if movie.get('premiereDateRussia'):
                if isinstance(movie.get('premiereDateRussia'), str):
                    movie['premiereDateRussia'] = datetime.strptime(movie.get('premiereDateRussia'), '%Y-%m-%d')
            dbb.running.update({'_id': movie.get('id')}, movie, upsert=True)
            logger.debug('Movie {} with id - {} was added to db'.format(movie.get('title'), movie.get('id')))


def del_not_running(j_json):
    list_current = []
    for i in j_json:
        list_current.append(i.get('id'))
    all_curent = dbb.running.find()
    for i in list(all_curent):
        if i.get('id') not in list_current:
            dbb.running.delete_one({'_id': i.get('id')})
            logger.debug('Movie with id - {} was deleted from db'.format(i.get('id')))


if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(module)s %(message)s",
        level=20)

    a = oop_work_with_api.ApiKinohod('https://api.kinohod.ru/api/data/2/5982bb5a-1d76-31f8-abd5-c4253474ecf3/')
    fill_running(a.get_json(a.running))
    del_not_running(a.get_json(a.running))