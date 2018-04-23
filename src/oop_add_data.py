from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src import oop_work_with_api
from datetime import datetime

from src.oop_test import Base, Distributors, CityInfo, Locations, NetworksInfo, Halls, \
                         SubwayInfo, Genres, LanguageInfo, Cinemas, Images, PhoneInfo, SubwaystationsCinemas, \
                         Goodies, CinemaGoodies, SeanceInfo, Format, SeanceFormat

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


def full_Goodies():
    data = {"Bar": "Есть кинобар",
            "Mall": "Расположен в ТЦ",
            "Cafe": "Есть зона кафе",
            "PlayArea": "Есть игровая зона",
            "Wi-Fi": "Есть бесплатный Wi-Fi",
            "CodeScanner": "Есть сканнер билетов",
            "PrintTerminal": "Есть терминал распечатки билетов",
            "IMAX": "Есть залы с экранами IMAX",
            "4DX": "Есть залы формата 4DX",
            "RealD": "Есть залы формата RealD",
            "DolbyAtmos": "Есть залы формата Dolby Atmos",
            "Coca-Cola": "В кинотеатре продается Coca-Cola",
            "Pepsi": "В кинотеатре продается Pepsi",
            "ComboSet": "В кинотеатре онлайн-продажи комбо"}
    for k in data:
        exist = session.query(Goodies).filter_by(good_title=k).first()
        if not exist:
            print(k)
            print(data.get(k))
            new_good = Goodies(good_title=k, name=data.get(k))
            session.add(new_good)
    session.commit()


def full_formats():
    data = {'на': 'Например, “на английском”, “на итальянском”, “на оригинальном”, “на гоблинcком (перевод Goblina)” и т.д.',
            'Мувик': 'Сеанс киносети Формула Кино, в нагрузку к которому идет детская игрушка',
            'КиноSale': 'Формат киносети Формула Кино - билет со сниженной стоимостью на сеансы фильмов, которые уже давно в прокате',
            'Для людей с аутизмом': 'Сеанс для людей с аутизмом',
            'IMAX': 'Сеанс в формате IMAX',
            'Dolby Atmos': 'Сеанс в формате Dolby Atmos',
            '4DX': 'Сеанс в формате 4DX',
            'RealD': 'Сеанс в формате RealD',
            '3D': 'Сеанс в формате 3D',
            'обычные': 'обычный сеанс'}
    for k in data:
        exist = session.query(Format).filter_by(format_name=k).first()
        if not exist:
            new_good = Format(format_name=k, description=data.get(k))
            session.add(new_good)
    session.commit()


def full_cinemas(df):
    for k,v in df.iterrows():
        exists = session.query(Cinemas).filter_by(cinema_id=v['id']).first()
        if not exists:
            new_cinema = Cinemas(cinema_id=v['id'],
                                 title=v['title'],
                                 shortTitle=v['shortTitle'],
                                 description=v['description'],
                                 website=v['website'],
                                 city_id=v['cityId'],
                                 address=v['address'],
                                 networkId=v['networkId'],
                                 isSale=v['isSale'],
                                 mall=v['mall'],
                                 timeToRefund=v['timeToRefund'],
                                 hallCount=v['hallCount'])
            new_location = Locations(cinema_id=v['id'],
                                     latitude=v['location'].get('latitude'),
                                     longitude=v['location'].get('longitude'))
            for photo in v['photo']:
                if photo.get('name'):
                    new_photos = Images(cinema_id=v['id'],
                                        rgb = photo.get('rgb'),
                                        name = photo.get('name'))
                    session.add(new_photos)
            for phone in v['phones']:
                if phone.get('number'):
                    new_phone = PhoneInfo(cinema_id=v['id'],
                                          number=phone.get('number'),
                                          description=phone.get('description'))
                    session.add(new_phone)
            for item in v['subwayStations']:
                if item.get('subwayId'):
                    new_subway_cinema = SubwaystationsCinemas(cinema_id=v['id'],
                                                              subwayId=item.get('subwayId'),
                                                              distance=item.get('distance'))
                    session.add(new_subway_cinema)
            for item in v['goodies']:
                if item:
                    new_goodies_cinema = CinemaGoodies(cinema_id=v['id'],
                                                       good_title = item)
                    session.add(new_goodies_cinema)
            session.add(new_cinema)
            session.add(new_location)
    session.commit()


def full_seances(df):
    for k,v in df.iterrows():
        exists = session.query(SeanceInfo).filter_by(seance_id=v['id']).first()
        if not exists:
            new_seance = SeanceInfo(seance_id=v['id'],
                                    movieId=v['movieId'],
                                    cinemaId=v['cinemaId'],
                                    date=datetime.strptime(v['date'], '%Y-%m-%d'),
                                    time=datetime.strptime(v['time'], '%H:%M'),
                                    startTime=datetime.strptime(v['startTime']+'00', '%Y-%m-%d %H:%M:%S%z'),
                                    hallId=v['hallId'],
                                    isSaleAllowed=v['isSaleAllowed'],
                                    minPrice=v['minPrice'],
                                    maxPrice=v['maxPrice'],
                                    maxSeatsInOrder=v['maxSeatsInOrder'],
                                    subtitleId=v['subtitleId'],
                                    languageId=v['languageId'],
                                    groupName=v['groupName'],
                                    groupOrder=v['groupOrder'])
            session.add(new_seance)
            for item in v['formats']:
                new_format_seanse = SeanceFormat(seance_id = v['id'],
                                                 format_name = item)
                session.add(new_format_seanse)
    session.commit()


if __name__ == '__main__':
    a = oop_work_with_api.ApiKinohod('https://api.kinohod.ru/api/data/2/5982bb5a-1d76-31f8-abd5-c4253474ecf3/')
    # full_cities(a.get_json(a.cities))
    # full_destibutors(a.get_json(a.distributors))
    # full_networks(a.get_json(a.networks))
    # full_halls(a.get_json(a.halls))
    # full_subways(a.get_json(a.subways))
    # full_genres(a.get_json(a.genres))
    # full_languages(a.get_json(a.languages))
    # full_cinemas(a.get_json(a.cinemas))
    # full_Goodies()
    # full_formats()
    full_seances(a.get_json(a.seances))