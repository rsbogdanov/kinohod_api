from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src import oop_work_with_api

from src.oop_test import Base, Distributors, CityInfo, Locations, NetworksInfo, Halls, \
                         SubwayInfo, Genres, LanguageInfo



engine = create_engine('sqlite:///../data/oop_test2.db', encoding='utf-8')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
session = DBSession()



def full_destibutors(df):
    for k,v in df.iterrows():
        exists = session.query(Distributors).filter_by(distributor_id=v['id']).first()
        if not exists:
            new_distr = Distributors(distributor_id=v['id'], distributor_name=v['name'])
            session.add(new_distr)
    session.commit()


def full_cities(df):
    for k,v in df.iterrows():
        exists = session.query(Locations).filter_by(city_id=v['id']).first()
        if not exists:
            new_cities = CityInfo(city_id =v['id'],
                                  title=v['title'],
                                  alias=v['title'],
                                  utcOffset=v['utcOffset'])
            new_location = Locations(city_id=v['id'],
                                     latitude=v['location'].get('latitude'),
                                     longitude=v['location'].get('longitude'))
            session.add(new_cities)
            session.add(new_location)
    session.commit()


def full_networks(df):
    for k,v in df.iterrows():
        exists = session.query(NetworksInfo).filter_by(network_id=v['id']).first()
        if not exists:
            new_network = NetworksInfo(network_id =v['id'],
                                  title=v['title'],
                                  isSale=v['isSale'])
            session.add(new_network)
    session.commit()


def full_halls(df):
    for k,v in df.iterrows():
        exists = session.query(Halls).filter_by(hall_id=v['id']).first()
        if not exists:
            new_hall = Halls(hall_id=v['id'],
                             cinemaId=v['cinemaId'],
                             title=v['title'],
                             description=v['description'],
                             placeCount=v['placeCount'],
                             isVIP=v['isVIP'],
                             isIMAX=v['isIMAX'],
                             orderScanner=v['orderScanner'],
                             ticketScanner=v['ticketScanner'])
            session.add(new_hall)
    session.commit()


def full_subways(df):
    for k,v in df.iterrows():
        exists = session.query(SubwayInfo).filter_by(subway_id=v['id']).first()
        if not exists:
            new_subway = SubwayInfo(subway_id=v['id'],
                                    title=v['title'],
                                    line=v['line'],
                                    color=v['color'],
                                    city_id=v['cityId'])
            new_location = Locations(subway_id=v['id'],
                                    latitude=v['location'].get('latitude'),
                                    longitude=v['location'].get('longitude'))
            session.add(new_subway)
            session.add(new_location)
    session.commit()



def full_genres(df):
    for k,v in df.iterrows():
        exists = session.query(Genres).filter_by(genre_id=v['id']).first()
        if not exists:
            new_genre = Genres(genre_id=v['id'], genre_name=v['name'])
            session.add(new_genre)
    session.commit()


def full_languages(df):
    for k,v in df.iterrows():
        exists = session.query(LanguageInfo).filter_by(language_id=v['id']).first()
        if not exists:
            new_lang = LanguageInfo(language_id=v['id'],
                                    greeting=v['greeting'],
                                    origTitle=v['origTitle'],
                                    title=v['title'],
                                    prepTitle=v['prepTitle'],
                                    shortTitle=v['shortTitle'])
            session.add(new_lang)
    session.commit()


if __name__ == '__main__':
    a = oop_work_with_api.ApiKinohod('https://api.kinohod.ru/api/data/2/5982bb5a-1d76-31f8-abd5-c4253474ecf3/')
    # full_cities(a.get_json(a.cities))
    # full_destibutors(a.get_json(a.distributors))
    # full_networks(a.get_json(a.networks))
    # full_halls(a.get_json(a.halls))
    # full_subways(a.get_json(a.subways))
    # full_genres(a.get_json(a.genres))
    full_languages(a.get_json(a.languages))