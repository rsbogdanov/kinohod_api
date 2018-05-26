from pymongo import MongoClient
import gridfs
from tqdm import tqdm
import datetime

import logging

logger = logging.getLogger(__name__)


#from flask import Flask, send_file

#import argparse
#from io import BytesIO
import mimetypes
import requests
#from PIL import Image



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



def add_image(image_url, filename):
    """add an image to mongo's gridfs"""
    # gridfs filename
    gridfs_filename = filename
    # guess the mimetype and request the image resource
    mime_type = mimetypes.guess_type(image_url)[0]
    r = requests.get(image_url, stream=True)
    # insert the resource into gridfs using the raw stream
    _id = fs.put(r.raw, contentType=mime_type, filename=gridfs_filename)
    logging.info("created new gridfs file {0} with id {1}".format(gridfs_filename, _id))

def get_image_url(ddict):
    image_url = 'http://{HOST}/p/1000x300/{ab}/{cd}/{uuid}.{ext}'.format(HOST='www.kinohod.ru',
                                                                         ab=ddict.get('name')[:2],
                                                                         cd=ddict.get('name')[2:4],
                                                                         uuid=ddict.get('name').split('.')[0],
                                                                         ext=ddict.get('name').split('.')[1])
    return image_url

def find_all_images_in_cinemas():
    res_f = dbb.cinemas.find({'photo.name': {"$ne": None}})
    print("Found {} images".format(len(list(res_f))))
    for i in tqdm(list(res_f)):
        for photo in i.get('photo'):
            image_url = get_image_url(photo)
            add_image(image_url, photo.get('name'))


def find_all_images_in_movies():
    res = []
    res_f = dbb.movies.find({'images.name': {"$ne": None}})
    for i in tqdm(list(res_f)):
        for image in i.get('images'):
            res.append(image)
    for i in tqdm(res):
        image_url = get_image_url(i)
        add_image(image_url, i.get('name'))


def find_all_posters_in_movies():
    res_f = dbb.movies.find({'poster.name': {"$ne": None}})
    for i in tqdm(list(res_f)):
        if i.get('poster'):
            image_url=get_image_url(i.get('poster'))
            add_image(image_url, i.get('name'))


def find_all_postersLand_in_movies():
    res_f = dbb.movies.find({'posterLandscape.name': {"$ne": None}})
    for i in tqdm(list(res_f)):
        if i.get('posterLandscape'):
            image_url = get_image_url(i.get('posterLandscape'))
            add_image(image_url, i.get('name'))


if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(module)s %(message)s",
        level=1)
    find_all_images_in_cinemas()
    find_all_images_in_movies()
    find_all_posters_in_movies()
    find_all_postersLand_in_movies()
