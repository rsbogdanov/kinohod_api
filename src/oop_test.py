import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Numeric, Date, DateTime, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from datetime import datetime

Base = declarative_base()

############################################################################
# Classes of data that we can directly get with the requests to api_kinohod#
############################################################################

class NetworksInfo(Base):
    __tablename__ = 'networksinfo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    network_id = Column(String, nullable=False)
    title = Column(String)
    isSale = Column(Boolean)

    cinemas = relationship("Cinemas", backref='networksinfo')


class Cinemas(Base):
    __tablename__ = 'cinemas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cinema_id = Column(Integer, nullable=False)
    title = Column(String)
    shortTitle = Column(String)
    description = Column(String)
    website = Column(String)
    city_id = Column(Integer, ForeignKey('cities.city_id'))
    address = Column(String)
    location = Column(String, ForeignKey('locations.cinema_id'))
    networkId = Column(Integer, ForeignKey('networksinfo.network_id'))
    isSale = Column(Boolean)
    mall = Column(String)
    timeToRefund = Column(Integer)
    hallCount = Column(Integer)
    subwayStations = Column(String)
    goodies = Column(String)
    photo = Column(String, ForeignKey('images.cinema_id'))
    phones = Column(String, ForeignKey('phones.cinema_id'))

    halls = relationship('Halls', backref="cinemas")


class Halls(Base):
    __tablename__ = 'halls'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hall_id = Column(Integer, nullable=False)
    cinemaId = Column(Integer, ForeignKey('cinemas.cinema_id'))
    title = Column(String)
    description = Column(String)
    placeCount = Column(Integer)
    isVIP = Column(Boolean)
    isIMAX = Column(Boolean)
    orderScanner = Column(Boolean)
    ticketScanner = Column(Boolean)


class MovieInfo(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, nullable=False)
    title = Column(String)
    duration = Column(Integer)
    originalTitle = Column(String)
    productionYear = Column(Integer)
    premiereDateRussia = Column(Date)
    premiereDateWorld = Column(Date)
    budget = Column(Numeric)
    countries = Column(String)
    producers = Column(String)
    companies = Column(String)
    directors = Column(String)
    actors = Column(String)
    genres = Column(String)
    annotationShort = Column(String)
    annotationFull = Column(String)
    ageRestriction = Column(String)
    grossRevenueRus = Column(Numeric)
    grossRevenueWorld = Column(Numeric)
    trailers = Column(String)
    images = Column(String)
    rating = Column(Numeric)
    imdbId = Column(String)
    externalTrailer = Column(String)
    poster = Column(Integer, ForeignKey('images.poster_movie_id'))
    posterLandscape = Column(Integer, ForeignKey('images.poster_land_movie_id'))
    countScreens = Column(Integer)
    countVotes = Column(Integer)
    countComments = Column(Integer)
    weight = Column(Integer)
    isDolbyAtmos = Column(Boolean)
    isImax = Column(Boolean)
    is4dx = Column(Boolean)
    isPresale = Column(Boolean)
    distributorId = Column(Integer, ForeignKey('distributors.distributor_id'))



class SeanceInfo(Base):
    __tablename__ = 'seances'
    id = Column(Integer, primary_key=True, autoincrement=True)
    seance_id = Column(Integer, nullable=False)
    movieId = Column(Integer, ForeignKey('movies.id'))
    cinemaId = Column(Integer, ForeignKey('cinemas.id'))
    date = Column(DateTime)
    time = Column(DateTime)
    startTime = Column(DateTime)
    hallId = Column(Integer, ForeignKey('halls.id'))
    formats = Column(String, ForeignKey('seance_format.seance_id'))
    isSaleAllowed = Column(Boolean)
    minPrice = Column(Numeric)
    maxPrice = Column(Numeric)
    maxSeatsInOrder = Column(Integer)
    subtitleId = Column(Integer)
    languageId = Column(Integer, ForeignKey('languages.id'))
    groupName = Column(String)
    groupOrder = Column(Integer)


class CityInfo(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, nullable=False)
    title = Column(String)
    alias = Column(String)
    utcOffset = Column(Integer)
    location = Column(Integer, ForeignKey('locations.city_id'))

    cinemas = relationship("Cinemas", backref="cities")
    subwaystation = relationship("SubwayInfo", backref="cities")


class SubwayInfo(Base):
    __tablename__ = 'subwaystations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    subway_id = Column(Integer, nullable=False)
    title = Column(String)
    line = Column(String)
    color = Column(String)
    location = Column(Integer, ForeignKey('locations.subway_id'))
    city_id = Column(Integer, ForeignKey('cities.city_id'))

    cinemas = relationship("Cinemas",
                           secondary='subwaystations_cinemas',
                           backref="subways")


class Genres(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True, autoincrement=True)
    genre_id = Column(String, nullable=False)
    genre_name = Column(String)
    movies = relationship("MovieInfo",
                          secondary="movies_genres",
                          backref="genr")


class Distributors(Base):
    __tablename__ = 'distributors'
    distributor_id = Column(Integer, primary_key=True, nullable=False)
    distributor_name = Column(String)
    movies = relationship("MovieInfo", backref="distributors")


class LanguageInfo(Base):
    __tablename__ = 'languages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    language_id = Column(String, nullable=False)
    title = Column(String)
    prepTitle = Column(String)
    origTitle = Column(String)
    shortTitle = Column(String)
    greeting = Column(String)


class Sources(Base):
    __tablename__ = 'sources'
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(Integer, nullable=False)
    description = Column(String)

    sourceentity = relationship("SourceEntityInfo", backref="sources")


class SourceEntityInfo(Base):
    __tablename__ = 'sourceentityinfo'
    id = Column(Integer, primary_key=True, autoincrement=True)

    sourceid = Column(Integer, ForeignKey('sources.id'))


##########################################################################
#Classes of creating tables with data, that we should construct without #
#direct request to API                                                   #
##########################################################################


class Actors(Base):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    actor_id = Column(Integer, nullable=False)
    actor_name = Column(String)
    movies = relationship("MovieInfo",
                          secondary="movies_actors",
                          backref="actor")


class Producers(Base):
    __tablename__ = 'producers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producer_id = Column(Integer, nullable=False)
    producer_name = Column(String)
    movies = relationship("MovieInfo",
                          secondary="movies_producers",
                          backref="producer")


class Directors(Base):
    __tablename__ = 'directors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    director_id = Column(Integer, nullable=False)
    director_name = Column(String)
    movies = relationship("MovieInfo",
                          secondary="movies_directors",
                          backref="director")


class Companies(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, nullable=False)
    company_name = Column(String)
    movies = relationship("MovieInfo",
                          secondary="movies_companies",
                          backref="company")


class Countryies(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    country_id = Column(Integer, nullable=False)
    country = Column(String)
    movies = relationship("MovieInfo",
                          secondary="movies_countries",
                          backref="country")


class Goodies(Base):
    __tablename__ = 'goodies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    good_title = Column(String, nullable=False)
    name = Column(String)
    cinema = relationship("Cinemas",
                          secondary="goodies_cinema",
                          backref="good")


class Locations(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    latitude = Column(Numeric, nullable=False)
    longitude = Column(Numeric, nullable=False)
    cinema_id = Column(Integer)
    city_id = Column(Integer)
    subway_id = Column(Integer)

    cinemas = relationship("Cinemas", backref="location_cinema")
    cities = relationship("CityInfo", backref="location_city")
    subways = relationship("SubwayInfo", backref="location_subway")



class Images(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, autoincrement=True)
    rgb = Column(String, nullable=False)
    name = Column(String, nullable=False)
    cinema_id = Column(Integer)
    movie_id = Column(Integer)
    poster_land_movie_id = Column(Integer)
    poster_movie_id = Column(Integer)
    image_movie_id = Column(Integer)
    preview_trailer_id = Column(Integer)
    source_trailer_id = Column(Integer)
    video_id = Column(Integer)

    cinemas = relationship("Cinemas", backref="images")
    movies = relationship("MovieInfo",
                          secondary="movies_images",
                          backref="images_movies")
    preview_trailer = relationship("TrailersInfo",
                          backref="images_prtrailers")
    videos = relationship("Videos",
                          backref="images_videos")




class Videos(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(Integer, ForeignKey('images.video_id'))
    duration = Column(Numeric)
    contentType = Column(String)
    trailer_source = Column(Integer)
    sourse_trailer_id = relationship("TrailersInfo",
                                     secondary="trailers_videos",
                                     backref="video_trailer")




class TrailersInfo(Base):
    __tablename__ = "trailers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    preview_image = Column(Integer, ForeignKey('images.preview_trailer_id'), nullable=False)
    videos = Column(Integer, nullable=False)
    source = Column(Integer, ForeignKey('videos.trailer_source'))
    movie = relationship("MovieInfo",
                         secondary="movies_trailers",
                         backref="trailer_video")


class MoviesTrailers(Base):
    __tablename__ = 'movies_trailers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey("movies.movie_id"))
    trailer_id = Column(Integer, ForeignKey("trailers.id"))


class TrailersVideos(Base):
    __tablename__ = 'trailers_videos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    trailer_id = Column(Integer, ForeignKey('trailers.id'))
    video_id = Column(Integer, ForeignKey('videos.id'))



##перенести##

####################################################
#associations tables for many-to-many relationships#
####################################################


class MoviesActors(Base):
    __tablename__ = 'movies_actors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    actor_id = Column(Integer, ForeignKey('actors.actor_id'))


class MoviesProducers(Base):
    __tablename__ = 'movies_producers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    producer_id = Column(Integer, ForeignKey('producers.producer_id'))


class MoviesDirectors(Base):
    __tablename__ = 'movies_directors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    director_id = Column(Integer, ForeignKey('directors.director_id'))


class MoviesCompanies(Base):
    __tablename__ = 'movies_companies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    companie_id = Column(Integer, ForeignKey('companies.company_id'))


class MoviesCountries(Base):
    __tablename__ = 'movies_countries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    country_id = Column(Integer, ForeignKey('countries.country_id'))


class MoviesGenres(Base):
    __tablename__ = 'movies_genres'
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    genre_id = Column(Integer, ForeignKey('genres.genre_id'))


class CinemaGoodies(Base):
    __tablename__ = 'goodies_cinema'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cinema_id = Column(Integer, ForeignKey('cinemas.cinema_id'))
    good_title = Column(String, ForeignKey('goodies.good_title'))


class PhoneInfo(Base):
    __tablename__ = 'phones'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cinema_id = Column(Integer)
    number = Column(String)
    description = Column(String)

    cinemas = relationship("Cinemas", backref="phone")


class SubwaystationsCinemas(Base):
    __tablename__ = 'subwaystations_cinemas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cinema_id = Column(Integer, ForeignKey('cinemas.cinema_id'))
    subwayId = Column(Integer, ForeignKey('subwaystations.subway_id'))
    distance = Column(Integer)


class PhotosCinemas(Base):
    __tablename__ = 'photos_cinemas'
    id = Column(Integer, primary_key=True)
    cinema_id = Column(Integer, ForeignKey('cinemas.id'))
    rgb = Column(String)
    name = Column(String)




class MoviesImages(Base):
    __tablename__ = 'movies_images'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    image_id = Column(Integer, ForeignKey('images.id'))


class Format(Base):
    __tablename__ = 'formats'
    id = Column(Integer, primary_key=True, autoincrement=True)
    format_name = Column(String)
    description = Column(String)



class SeanceFormat(Base):
    __tablename__ = 'seance_format'
    id = Column(Integer, primary_key=True)
    seance_id = Column(Integer)
    format_name = Column(String)
    seance = relationship("SeanceInfo", backref='seances')


engine = create_engine('sqlite:///../data/oop_test2.db', encoding='utf-8')

Base.metadata.create_all(engine)
