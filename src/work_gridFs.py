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



client = MongoClient('mongodb://myUserAdmin:RomA48917050@localhost:27017/')
dbb = client['Kinohod']
db = client['Kinohod_files']
fs = gridfs.GridFS(db)



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
    res_f = dbb.cinemas.find({'photo': {'$ne': {'name': None, 'rgb': None}}})
    print(len(list(res_f)))
    for i in tqdm(list(res_f)):
        if i.get('photo') != {'name': None, 'rgb': None}:
            for photo in i.get('photo'):
                image_url = get_image_url(photo)
                add_image(image_url, photo.get('name'))


def find_all_images_in_movies():
    res = []
    for i in tqdm(list(dbb.movies.find({'images': {'$ne': {'name': None, 'rgb': None}}}))):
        for image in i.get('images'):
            res.append(image)
    for i in tqdm(res):
        image_url = get_image_url(i)
        add_image(image_url, i.get('name'))


def find_all_posters_in_movies():
    for i in tqdm(list(dbb.movies.find({'poster': {'$ne': {'name': None, 'rgb': None}}}))):
        if i.get('poster'):
            image_url=get_image_url(i.get('poster'))
            add_image(image_url, i.get('name'))


def find_all_postersLand_in_movies():
    for i in tqdm(list(dbb.movies.find({'posterLandscape': {'$ne': {'name': None, 'rgb': None}}}))):
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