from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.oop_test import Base, Images, MyCompanies, MyActors, MyDirectors, MyProducers, \
    MoviesProducers, MoviesDirectors, MoviesCompanies, MoviesActors
from src import oop_add_data


def check_is_time(obj):
    data = '1700-01-01'
    if obj:
        data = obj
    return data


def add_image(df_line, rgb, name, image_type, session):
    _dict_image = {'cinema_id': None, 'movie_id': None, 'poster_land_movie_id': None, 'image_movie_id': None,
                   'preview_trailer_id': None, 'source_trailer_id': None, 'video_id': None, 'poster_movie_id': None,
                   image_type: df_line['id']}
    new_image = Images(rgb=rgb,
                       name=name,
                       cinema_id=_dict_image.get('cinema_id'),
                       poster_movie_id=_dict_image.get('poster_movie_id'),
                       poster_land_movie_id=_dict_image.get('poster_land_movie_id'),
                       image_movie_id=_dict_image.get('image_movie_id'),
                       preview_trailer_id=_dict_image.get('preview_trailer_id'),
                       source_trailer_id=_dict_image.get('source_trailer_id'),
                       video_id=_dict_image.get('video_id'))
    session.add(new_image)


def fill_common_dict_tables(field_name, df_string, session):
    if df_string.get(field_name):
        for item in df_string.get(field_name):
            exists = session.query(_dict[field_name]).filter_by(field_id=item.get('id')).first()
            if not exists:
                new_company = _dict[field_name](field_id=item.get('id'),
                                                name=item.get('name'))
                session.add(new_company)
            new_mtm = _dict_mtm[field_name](movie_id=df_string['id'],
                                            field_id=item.get('id'))
            session.add(new_mtm)


_dict = {"companies": MyCompanies,
         "actors": MyActors,
         "producers": MyProducers,
         "directors": MyDirectors}

_dict_mtm = {"companies": MoviesCompanies,
             "actors": MoviesActors,
             "producers": MoviesProducers,
             "directors": MoviesDirectors}
