import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Numeric, Date, DateTime, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Halls(Base):
    __tablename__ = 'halls'
    id = Column(Integer, primary_key=True)
    cinemaId = Column(Integer, ForeignKey('cinemas.id'))
    title = Column(String)
    description = Column(String)
    placeCount = Column(Integer)
    isVIP = Column(Boolean)
    isIMAX = Column(Boolean)
    orderScanner = Column(Boolean)
    ticketScanner = Column(Boolean)


class Actors(Base):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)
    actor_name = Column(String)


class Producers(Base):
    __tablename__ = 'producers'
    id = Column(Integer, primary_key=True)
    producer_name = Column(String)


class Genres(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    genre_name = Column(String)


class Directors(Base):
    __tablename__ = 'directors'
    id = Column(Integer, primary_key=True)
    director_name = Column(String)


class Companies(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    company_name = Column(String)


class Cinemas(Base):
    __tablename__ = 'cinemas'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    shortTitle = Column(String)
    description = Column(String)
    website = Column(String)
    cityId = Column(Integer, ForeignKey('cities.id'))
    address = Column(String)
    location = Column(String, ForeignKey('locations_cinemas.cinema_id'))
    networkId = Column(Integer, ForeignKey('networksinfo.id'))
    isSale = Column(Boolean)
    mall = Column(String)
    timeToRefund = Column(Integer)
    hallCount = Column(Integer)
    subwayStations = Column(String, ForeignKey('subwaystations_cinemas.cinema_id'))
    goodies = Column(String, ForeignKey('goodies_cinema.id'))
    photo = Column(String, ForeignKey('photos_cinemas.cinema_id'))
    phones = Column(String, ForeignKey('phones.cinema_id'))


class CinemaGoodies(Base):
    __tablename__ = 'goodies_cinema'
    id = Column(Integer, primary_key=True)
    cinema_id = Column(Integer, ForeignKey('cinemas.id'))
    good_id = Column(Integer, ForeignKey('goodies.id'))


class Goodies(Base):
    __tablename__ = 'goodies'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class NetworksInfo(Base):
    __tablename__ = 'networksinfo'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    isSale = Column(Boolean)


class MovieInfo(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    duration = Column(Integer)
    originalTitle = Column(String)
    productionYear = Column(Integer)
    premiereDateRussia = Column(Date)
    premiereDateWorld = Column(Date)
    budget = Column(Numeric)
    countries = Column(String, ForeignKey('movies_countries.movie_id'))
    producers = Column(Integer, ForeignKey('movies_producers.movie_id'))
    companies = Column(Integer, ForeignKey('movies_companies.movie_id'))
    directors = Column(Integer, ForeignKey('movies_directors.movie_id'))
    actors = Column(Integer, ForeignKey('movies_actors.movie_id'))
    genres = Column(Integer, ForeignKey('movies_genres.movie_id'))
    annotationShort = Column(String)
    annotationFull = Column(String)
    ageRestriction = Column(String)
    grossRevenueRus = Column(Numeric)
    grossRevenueWorld = Column(Numeric)
    trailers = Column(String, ForeignKey('movies_trailers.movie_id'))
    images = Column(String, ForeignKey('movies_images.movie_id'))
    rating = Column(Numeric)
    imdbId = Column(String)
    externalTrailer = Column(String)
    poster = Column(Integer, ForeignKey('posters_images.movie_id'))
    posterLandscape = Column(Integer, ForeignKey('posterslands_images.movie_id'))
    countScreens = Column(Integer)
    countVotes = Column(Integer)
    countComments = Column(Integer)
    weight = Column(Integer)
    isDolbyAtmos = Column(Boolean)
    isImax = Column(Boolean)
    is4dx = Column(Boolean)
    isPresale = Column(Boolean)
    distributorId = Column(Integer, ForeignKey('distributors.id'))


class SeanceInfo(Base):
    __tablename__ = 'seances'
    id = Column(Integer, primary_key=True)
    movieId = Column(Integer, ForeignKey('movies.id'))
    cinemaId = Column(Integer, ForeignKey('cinemas.id'))
    date = Column(Date)
    time = Column(String)
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
    id = Column(Integer, primary_key=True)
    title = Column(String)
    alias = Column(String)
    utcOffset = Column(Integer)
    location = Column(Integer, ForeignKey('city_location.city_id'))


class SubwayInfo(Base):
    __tablename__ = 'subwaystations'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    line = Column(String)
    color = Column(String)
    location = Column(Integer, ForeignKey('subwaystations_location.id'))
    cityId = Column(Integer, ForeignKey('cities.id'))


class SubwaystationsLocation(Base):
    __tablename__ = 'subwaystations_location'
    id = Column(Integer, primary_key=True)
    subwaystations_id = Column(Integer, ForeignKey('subwaystations.id'))
    latitude = Column(Numeric)
    longitude = Column(Numeric)



class LanguageInfo(Base):
    __tablename__ = 'languages'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    prepTitle = Column(String)
    origTitle = Column(String)
    shortTitle = Column(String)
    greeting = Column(String)


class PhoneInfo(Base):
    __tablename__ = 'phones'
    id = Column(Integer, primary_key=True)
    cinema_id = Column(Integer)
    number = Column(String)
    description = Column(String)


class LocationsCinemas(Base):
    __tablename__ = 'locations_cinemas'
    cinema_id = Column(Integer, primary_key=True)
    latitude = Column(Numeric)
    longitude = Column(Numeric)


class SubwaystationsCinemas(Base):
    __tablename__ = 'subwaystations_cinemas'
    id = Column(Integer, primary_key=True)
    cinema_id = Column(Integer, ForeignKey('cinemas.id'))
    subwayId = Column(Integer, ForeignKey('subwaystations.id'))
    distance = Column(Integer)


class PhotosCinemas(Base):
    __tablename__ = 'photos_cinemas'
    id = Column(Integer, primary_key=True)
    cinema_id = Column(Integer, ForeignKey('cinemas.id'))
    rgb = Column(String)
    name = Column(String)


class MoviesCountries(Base):
    __tablename__ = 'movies_countries'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    country_id = Column(Integer, ForeignKey('countries.id'))


class Countryies(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True)
    country = Column(String)


class Distributors(Base):
    __tablename__ = 'distributors'
    id = Column(Integer, primary_key=True,autoincrement=True)
    distributors = Column(String)


class MoviesProducers(Base):
    __tablename__ = 'movies_producers'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    producer_id = Column(Integer, ForeignKey('producers.id'))


class MoviesCompanies(Base):
    __tablename__ = 'movies_companies'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    companie_id = Column(Integer, ForeignKey('companies.id'))


class MoviesDirectors(Base):
    __tablename__ = 'movies_directors'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    director_id = Column(Integer, ForeignKey('directors.id'))


class MoviesActors(Base):
    __tablename__ = 'movies_actors'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    actor_id = Column(Integer, ForeignKey('actors.id'))


class MoviesGenres(Base):
    __tablename__ = 'movies_genres'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    genre_id = Column(Integer, ForeignKey('genres.id'))


class MoviesTrailers(Base):
    __tablename__ = 'movies_trailers'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    preview_id = Column(Integer, ForeignKey('moviestrailers_preview.id'))
    videos_ids = Column(String, ForeignKey('moviestrailers_videos.id'))
    source = Column(String, ForeignKey('movies_trailers_source.id'))


class MoviesTrailersVideos(Base):
    __tablename__ = 'moviestrailers_videos'
    id = Column(Integer, primary_key=True)
    movietrailer_id = Column(Integer, ForeignKey('movies_trailers.id'))
    movietrailer_filename = Column(Integer, ForeignKey('movies_trailers_videos_filename.id'))
    movietrailer_duration = Column(Numeric)
    movietrailer_contenttype = Column(String)


class MoviesTrailersVideosFilename(Base):
    __tablename__ = 'movies_trailers_videos_filename'
    id = Column(Integer, primary_key=True)
    rgb = Column(String)
    name = Column(String)


class MoviesTrailersPreview(Base):
    __tablename__ = 'moviestrailers_preview'
    id = Column(Integer, primary_key=True)
    rgb = Column(String)
    name = Column(String)


class MoviesTrailersSource(Base):
    __tablename__ = 'movies_trailers_source'
    id = Column(Integer, primary_key=True)
    source_filename = Column(Integer, ForeignKey('movies_trailers_source_filename.id'))
    source_duration = Column(Numeric)
    source_contenttype = Column(String)


class MoviesTrailersVideosSource(Base):
    __tablename__ = 'movies_trailers_source_filename'
    id = Column(Integer, primary_key=True)
    rgb = Column(String)
    name = Column(String)


class MoviesImages(Base):
    __tablename__ = 'movies_images'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    rgb = Column(String)
    name = Column(String)



class PostersImages(Base):
    __tablename__ = 'posters_images'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    rgb = Column(String)
    name = Column(String)


class PostersLandsImages(Base):
    __tablename__ = 'posterslands_images'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    rgb = Column(String)
    name = Column(String)


class Format(Base):
    __tablename__ = 'formats'
    id = Column(Integer, primary_key=True)
    description = Column(String)


class SeanceFormat(Base):
    __tablename__ = 'seance_format'
    id = Column(Integer, primary_key=True)
    seance_id = Column(Integer, ForeignKey('seances.id'))
    format_id = Column(Integer, ForeignKey('formats.id'))


class CitiesLocations(Base):
    __tablename__ = 'city_location'
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('cities.id'))
    latitude = Column(Numeric)
    longitude = Column(Numeric)


engine = create_engine('sqlite:///../data/oop_test2.db', encoding='utf-8')


Base.metadata.create_all(engine)