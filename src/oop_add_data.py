from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src import oop_work_with_api
from datetime import datetime
from tqdm import tqdm
import logging

logger = logging.getLogger(__name__)



from src.oop_test import Base, Distributors, CityInfo, Locations, NetworksInfo, Halls, \
                         SubwayInfo, Genres, LanguageInfo, Cinemas, Images, PhoneInfo, SubwaystationsCinemas, \
                         Goodies, CinemaGoodies, SeanceInfo, Format, SeanceFormat, MovieInfo, MoviesActors, \
                         MoviesCompanies, MoviesCountries, MoviesDirectors, MoviesProducers, \
                         MyCompanies, MyActors, MyProducers, MyDirectors, Videos

engine = create_engine('sqlite:///../data/oop_test2.db', encoding='utf-8')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
session = DBSession()


def full_destibutors(df):
    new, old = 0, 0
    for v in df:
        exists = session.query(Distributors).filter_by(distributor_id=v['id']).first()
        if not exists:
            new += 1
            new_distr = Distributors(distributor_id=v['id'], distributor_name=v['name'])
            session.add(new_distr)
        else:
            old += 1
            if old % 5 == 0:
                logger.debug("Distributor id: {} already  exists".format(v['id']))
        session.commit()
    logger.debug("There were added {} distributors, {} distributors already were been ".format(new, old))


def full_cities(df):
    new, old = 0, 0
    for v in df:
        exists = session.query(Locations).filter_by(city_id=v['id']).first()
        if not exists:
            new += 1
            new_cities = CityInfo(city_id =v['id'],
                                  title=v['title'],
                                  alias=v['title'],
                                  utcOffset=v['utcOffset'])
            new_location = Locations(city_id=v['id'],
                                     latitude=v['location'].get('latitude'),
                                     longitude=v['location'].get('longitude'))
            session.add(new_cities)
            session.add(new_location)
        else:
            old += 1
            if old % 10 == 0:
                logger.debug("City id: {} already  exists".format(v['id']))
        session.commit()
    logger.debug("There were added {} cities, {} cities already were been in base".format(new, old))

def full_networks(df):
    new, old = 0, 0
    for v in df:
        exists = session.query(NetworksInfo).filter_by(network_id=v['id']).first()
        if not exists:
            new += 1
            new_network = NetworksInfo(network_id =v['id'],
                                  title=v['title'],
                                  isSale=v['isSale'])
            session.add(new_network)
        else:
            old += 1
            if old % 10 == 0:
                logger.debug("Network id: {} already  exists".format(v['id']))
        session.commit()
    logger.debug("There were added {} networks, {} networks already were been in base".format(new, old))



def full_halls(df):
    old, new = 0, 0
    for v in df:
        exists = session.query(Halls).filter_by(hall_id=v['id']).first()
        if not exists:
            new += 1
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
        else:
            old += 1
            if old % 5 == 0:
                logger.debug("Hall id: {} already  exists".format(v['id']))
        session.commit()
    logger.debug("There were added {} halls, {} halls already were been in base".format(new, old))

def full_subways(df):
    new, old = 0, 0
    for v in df:
        exists = session.query(SubwayInfo).filter_by(subway_id=v['id']).first()
        if not exists:
            new += 1
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
        else:
            old += 1
            if old % 5 == 0:
                logger.debug("Subway id: {} already  exists".format(v['id']))
        session.commit()
    logger.debug("There were added {} subway stations, {} subway stations already were been in base".format(new, old))




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
    for k,v in tqdm(df.iterrows()):
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
    new, old = 0, 0
    for v in tqdm(df[55000:]):
        exists = session.query(SeanceInfo).filter_by(seance_id=v['id']).first()
        if not exists:
            new += 1
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
                new_format_seanse = SeanceFormat(seance_id=v['id'],
                                                 format_name=item)
                session.add(new_format_seanse)
        else:
            old += 1
            if old % 10 == 0:
                logger.debug("seance id: {} already  exists".format(v['id']))
        session.commit()
    logger.debug("There were added {} seances, {} seance already were been in base".format(new, old))

def full_movies(df):
    new, old = 0, 0
    for v in tqdm(df):
        exists = session.query(MovieInfo).filter_by(movie_id=v['id']).first()
        if not exists:
            new += 1
            new_movie=MovieInfo(movie_id=v['id'],
                                title=v['title'],
                                duration=v['duration'],
                                originalTitle=v['originalTitle'],
                                productionYear=v['productionYear'],
                                premiereDateRussia=datetime.strptime(check_is_time(v['premiereDateRussia']),'%Y-%m-%d'),
                                premiereDateWorld=datetime.strptime(check_is_time(v['premiereDateWorld']),'%Y-%m-%d'),
                                budget=v['budget'],
                                annotationShort=v['annotationShort'],
                                annotationFull=v['annotationFull'],
                                ageRestriction=v['ageRestriction'],
                                grossRevenueRus=v['grossRevenueRus'],
                                grossRevenueWorld=v['grossRevenueWorld'],
                                rating=v['rating'],
                                imdbId=v['imdbId'],
                                externalTrailer=v['externalTrailer'],
                                countScreens=v['countScreens'],
                                countVotes=v['countVotes'],
                                countComments=v['countComments'],
                                weight=v['weight'],
                                isDolbyAtmos=v['isDolbyAtmos'],
                                isImax=v['isImax'],
                                is4dx=v['is4dx'],
                                isPresale=v['isPresale'],
                                distributorId=v['distributorId'])
            session.add(new_movie)
            for k in _dict.keys():
                fill_common_dict_tables(k, v)

            if v['countries']:
                for item in v['countries']:
                    new_country_movie = MoviesCountries(movie_id=v['id'],
                                                        country=item)
                    session.add(new_country_movie)

            if v['poster'].get('name') and v['poster'].get('rgb'):
                add_image(v, rgb=v['poster'].get('rgb'),
                          name=v['poster'].get('name'), image_type='poster_movie_id')

            if v['posterLandscape'].get('name') and v['posterLandscape'].get('rgb'):
                add_image(v, rgb=v['posterLandscape'].get('rgb'),
                          name=v['posterLandscape'].get('name'), image_type='poster_land_movie_id')

            if v['images']:
                for item in v['images']:
                    if item.get('name') and item.get('rgb'):
                        add_image(v, name=item.get('name'), rgb=item.get('rgb'),
                                        image_type='image_movie_id')

            if v['trailers']:
                for item in v['trailers']:
                    if item.get('preview'):
                        add_image(df_line=v, image_type='preview_trailer_id', rgb=item.get('preview').get('rgb'),
                                  name=item.get('preview').get('name'))
                    if item.get('source'):
                        new_v_source = Videos(trailer_source=v['id'],
                                              filename=item.get('source').get('filename'),
                                              duration=item.get('source').get('duration'),
                                              contentType=item.get('source').get('contentType'))
                        session.add(new_v_source)
                    if item.get('videos'):
                        for video in item.get('videos'):
                            new_v = Videos(trailer_id=v['id'],
                                           filename=video.get('filename'),
                                           duration=video.get('duration'),
                                           contentType=video.get('contentType'))
                            session.add(new_v)
        else:
            old += 1
            if old % 10 == 0:
                logger.debug("movie id: {} already  exists".format(v['id']))
        session.commit()
    logger.debug("There were added {} movies, {} movies already were been in base".format(new, old))






def check_is_time(obj):
    data = '1700-01-01'
    if obj:
        data = obj
    return data


def add_image(df_line, rgb, name, image_type):
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


def fill_common_dict_tables(field_name, df_string):
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


if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(module)s %(message)s",
        level=10)

    a = oop_work_with_api.ApiKinohod('https://api.kinohod.ru/api/data/2/5982bb5a-1d76-31f8-abd5-c4253474ecf3/')
    # full_cities(a.get_json(a.cities))
    # full_destibutors(a.get_json(a.distributors))
    # full_networks(a.get_json(a.networks))
    # full_halls(a.get_json(a.halls))
    full_subways(a.get_json(a.subways))
    # full_genres(a.get_json(a.genres))
    # full_languages(a.get_json(a.languages))
    # full_cinemas(a.get_json(a.cinemas))
    # full_Goodies()
    # full_formats()
    # full_movies(a.get_json(a.movies))
    full_seances(a.get_json(a.seances))
