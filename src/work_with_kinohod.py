import pandas as pd
import json
import utils
from tqdm import tqdm
import requests


URL = 'https://api.kinohod.ru/api/data/2/5982bb5a-1d76-31f8-abd5-c4253474ecf3/'
MOVIES_SOON = 'movies/soon.json'
SEANCES = 'seances.json'
CITIES = 'cities.json'
SEANCES_SOON = '/seances/soon.json'


def get_report(url):
    link = URL + url
    headers = {"Accept-Encoding": "json"}
    movies_soon = requests.get(link, headers=headers)
    if movies_soon.status_code == 200:
        print(movies_soon.status_code)
        movies_soon_json = movies_soon.json()
        return pd.DataFrame(movies_soon_json)
    else: print('error')

def get_report_for_all_cities(url, con):
    for city in get_all_cities(con):
        link = '{URL}/city/{id}/{l_url}'.format(URL=URL, id=city, l_url=url)
        headers = {"Accept-Encoding": "json"}
        seances_soon = requests.get(link, headers=headers)
        if seances_soon.status_code == 200:
            print(seances_soon.status_code)
            seances_soon_json = seances_soon.json()
            a = pd.DataFrame(seances_soon_json)
            full_seances(a, con)
            print("For city_id: {} were added {} seances".format(city, len(a)))
        else:
            print('error')



def create_table(param_table, name_table, con):
    cur = con.cursor()
    query = """
            CREATE TABLE if not exists '{name_table}'
                ({param_table});""".format(param_table = param_table, name_table = name_table)
    cur.execute(query)
    con.commit()


def create_df_with_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as j_file:
        a = json.load(j_file)
    df = pd.DataFrame(a)
    return df



def full_films(df,con):
    cur = con.cursor()
    for i, k in df.iterrows():
        params = {'movieid': k.id,
                'title': k.title,
                'originalTitle': k.originalTitle,
                'duration': k.duration,
                'productionYear': k.productionYear,
                'premiereDateRussia': k.premiereDateRussia,
                'premiereDateWorld': k.premiereDateWorld,
                'budget': k.budget,
                'annotationShort': k.annotationShort,
                'annotationFull': k.annotationFull,
                'ageRestriction': k.ageRestriction,
                'grossRevenueRus': k.grossRevenueRus,
                'grossRevenueWorld': k.grossRevenueWorld,
                'rating': k.rating,
                'imdbId': k.imdbId,
                'externalTrailer': k.externalTrailer,
                'countScreens': k.countScreens,
                'countVotes': k.countVotes,
                'countComments': k.countComments,
                'weight': k.weight,
                'isDolbyAtmos': k.isDolbyAtmos,
                'isImax': k.isImax,
                'is4dx': k.is4dx,
                'isPresale': k.isPresale,
                'distributorId': k.distributorId}
        query = """
    INSERT INTO films
            (movieid,title,originalTitle,duration,
            productionYear,premiereDateRussia,premiereDateWorld,
            budget,annotationShort,annotationFull,ageRestriction,
            grossRevenueRus,grossRevenueWorld,rating,imdbId,
            externalTrailer,countScreens,countVotes,
            countComments,weight,isDolbyAtmos,isImax,
            is4dx,isPresale,distributorId)
    VALUES (:movieid,:title,:originalTitle,:duration,
            :productionYear,:premiereDateRussia,:premiereDateWorld,
            :budget,:annotationShort,:annotationFull,:ageRestriction,
            :grossRevenueRus,:grossRevenueWorld,:rating,:imdbId,
            :externalTrailer,:countScreens,:countVotes,
            :countComments,:weight,:isDolbyAtmos,
            :isImax,:is4dx,:isPresale,:distributorId)"""
        cur.execute(query,params)
    conn.commit()

def full_cinema(df,con):
    cur = con.cursor()
    for i , k in df.iterrows():
        geo = (k.location.get("longitude"), k.location.get("latitude"))
        geo = ";".join(map(str, geo))
        params = {'cinema_id': k.id,
                  'title': k.title,
                  'shortTitle': k.shortTitle,
                  'description': k.description,
                  'website': k.website,
                  'cityId': k.cityId,
                  'address': k.address,
                  'location': geo,
                  'networkId': k.networkId,
                  'isSale': k.isSale,
                  'mall': k.mall,
                  'timeToRefund': k.timeToRefund,
                  'hallCount': k.hallCount}
        query = """
            INSERT INTO cinemas
                        (cinema_id,title,shortTitle,description,
                        website,cityId,address,location,
                        networkId,isSale,mall,timeToRefund,
                        hallCount)
            VALUES
                        (:cinema_id,:title,:shortTitle,:description,
                        :website,:cityId,:address,:location,
                        :networkId,:isSale,:mall,:timeToRefund
                        ,:hallCount)"""
        cur.execute(query, params)
    conn.commit()


def full_cities(df,con):
    cur = con.cursor()
    for i, k in df.iterrows():
        geo = (k.location.get("longitude"), k.location.get("latitude"))
        geo = ";".join(map(str, geo))
        params = {"cityid": k.id,
                  "title": k.title,
                  "location": geo,
                  "utcOffset": k.utcOffset,
                  "alias": k.alias}
        query = """
        INSERT INTO cities (cityid,title,location,utcOffset,alias)
        SELECT :cityid,:title,:location,:utcOffset,:alias
        WHERE NOT EXISTS
            (SELECT 1 FROM cities WHERE cityid = :cityid)"""
        cur.execute(query, params)
    conn.commit()


def full_seances(df,con):
    cur = con.cursor()
    for i, k in df.iterrows():
        params = {'seanc_id': k.id,
                  'movieId': k.movieId,
                  'cinemaId': k.cinemaId,
                  'date': k.date,
                  'time': k.time,
                  'startTime': k.startTime,
                  'hallId': k.hallId,
                  'isSaleAllowed': k.isSaleAllowed,
                  'minPrice': k.minPrice,
                  'maxPrice': k.maxPrice,
                  'maxSeatsInOrder': k.maxSeatsInOrder,
                  'subtitleId': k.subtitleId,
                  'languageId': k.languageId,
                  'groupName': k.groupName,
                  'groupOrder': k.groupOrder}
        query = """
        INSERT INTO seances
                (seanc_id,movieId,cinemaId,date,
                time,startTime,hallId,isSaleAllowed,
                minPrice,maxPrice,maxSeatsInOrder,subtitleId,
                languageId,groupName,groupOrder)
        SELECT
                :seanc_id,:movieId,:cinemaId,:date,
                :time,:startTime,:hallId,:isSaleAllowed,
                :minPrice,:maxPrice,:maxSeatsInOrder,:subtitleId,
                :languageId,:groupName,:groupOrder
        WHERE NOT EXISTS(SELECT 1 FROM seances WHERE seanc_id = :seanc_id)"""
        cur.execute(query, params)
    conn.commit()

def full_halls(df,con):
    cur = con.cursor()
    for i, k in df.iterrows():
        params = {'hall_id': k.id,
                  'cinemaId': k.cinemaId,
                  'title': k.title,
                  'description': k.description,
                  'placeCount': k.placeCount,
                  'isVIP': k.isVIP,
                  'isIMAX': k.isIMAX,
                  'orderScanner': k.orderScanner,
                  'ticketScanner': k.ticketScanner}
        query = """
        INSERT INTO halls
            (hall_id,cinemaId,title,description,
            placeCount,isVIP,isIMAX,
            orderScanner,ticketScanner)
        VALUES
            (:hall_id,:cinemaId,:title,:description,
            :placeCount,:isVIP,:isIMAX,
            :orderScanner,:ticketScanner)"""
        cur.execute(query, params)
    con.commit()



def add_actors(df,con):
    cur = con.cursor()
    for i, k in df.iterrows():
        if k.actors:
            for item in k.actors:
                params = {'id':item.get('id'),
                          'actor':item.get('name')}
                query = """
                INSERT INTO actors (actor_id, actor_name) 
                SELECT :id, :actor 
                WHERE NOT EXISTS(SELECT 1 FROM actors WHERE actor_id = :id);"""
                cur.execute(query,params)
    con.commit()


def add_producers(df,con):
    cur = con.cursor()
    for i, k in df.iterrows():
        if k.producers:
            for item in k.producers:
                params = {'id':item.get('id'),
                          'producer':item.get('name')}
                query = """
                INSERT INTO producers (producer_id, producer_name) 
                SELECT :id, :producer 
                WHERE NOT EXISTS(SELECT 1 FROM producers WHERE producer_id = :id);"""
                cur.execute(query,params)
    con.commit()


def add_companies(df,con):
    cur = con.cursor()
    for i, k in df.iterrows():
        if k.companies:
            for item in k.companies:
                params = {'id': item.get('id'),
                          'company': item.get('name')}
                query = """
                    INSERT INTO companies (company_id, company_name) 
                    SELECT :id, :company 
                    WHERE NOT EXISTS(SELECT 1 FROM companies WHERE company_id = :id);"""
                cur.execute(query, params)
    con.commit()


def add_directors(df, con):
    cur = con.cursor()
    for i, k in df.iterrows():
        if k.directors:
            for item in k.directors:
                params = {'id': item.get('id'),
                          'director': item.get('name')}
                query = """
                        INSERT INTO directors (director_id, director_name) 
                        SELECT :id, :director 
                        WHERE NOT EXISTS(SELECT 1 FROM directors WHERE director_id = :id);"""
                cur.execute(query, params)
    con.commit()


def add_genres(df, con):
    cur = con.cursor()
    for i, k in df.iterrows():
        if k.genres:
            for item in k.genres:
                params = {'id': item.get('id'),
                          'genre': item.get('genre')}
                query = """
                        INSERT INTO genres (genre_id, genre_name) 
                        SELECT :id, :genre 
                        WHERE NOT EXISTS(SELECT 1 FROM genres WHERE genre_id = :id);"""
                cur.execute(query, params)
    con.commit()



def country_for_film(df,con):
    cur = con.cursor()
    for i, k in df.iterrows():
        if k.countries:
            for item in k.countries:
                query = """
                    INSERT INTO film_countries (film_id, country)
                    SELECT :film_id, :country
                    WHERE NOT EXISTS(SELECT 1 FROM film_countries WHERE film_id = :film_id AND country = :country)
                    """
                cur.execute(query,{'film_id':k.id, 'country':item})
    con.commit()



def add_goodies(df,con):
    cur=con.cursor()
    for i, k in df[['id','goodies']].iterrows():
        if k.goodies:
            for item in k.goodies:
                query = """
                        INSERT INTO cinema_goodies (cinema_id, good)
                        SELECT :cinema_id, :good
                        WHERE NOT EXISTS(SELECT 1 FROM cinema_goodies WHERE cinema_id = :cinema_id AND good = :good)
                        """
                cur.execute(query, {'cinema_id': k.id, 'good': item})
    con.commit()



def add_phones(df,con):
    cur = con.cursor()
    for i, k in df[['id', 'phones']].iterrows():
        if k.phones:
            for item in k.phones:
                params = {'cinema_id': k.id,
                          'phone': item.get('number'),
                          'description': item.get('description')}
                query = """
                    INSERT INTO phones (cinema_id, phone, description)
                    SELECT :cinema_id, :phone, :description
                    WHERE NOT EXISTS
                    (SELECT 1 FROM phones WHERE cinema_id = :cinema_id 
                            AND phone=:phone)"""
                cur.execute(query, params)
    con.commit()



def producer_for_film(df,con):
    cur = con.cursor()
    for i, k in df[['id', 'producers']].iterrows():
        if k.producers:
            for item in k.producers:
                query = """
                INSERT INTO film_producer (film_id, producer_id)
                SELECT :film_id, :producer_id
                WHERE NOT EXISTS(SELECT 1 FROM film_producer WHERE film_id = :film_id AND producer_id = :producer_id)"""
                cur.execute(query, {"film_id":k.id , "producer_id":item.get('id')})
    con.commit()


def companies_to_film(df,con):
    cur = con.cursor()
    for i, k in df.iterrows():
        if k.companies:
            for item in k.companies:
                query = """
                        INSERT INTO film_companies (film_id, company_id)
                        SELECT :film_id, :company_id
                        WHERE NOT EXISTS(SELECT 1 FROM film_companies WHERE film_id = :film_id 
                                                            AND company_id = :company_id)"""
                cur.execute(query, {"film_id": k.id, "company_id": item.get('id')})
    con.commit()



def directors_to_film(df,con):
    cur = con.cursor()
    for i, k in df[['id', 'directors']].iterrows():
        if k.directors:
            for item in k.directors:
                query = """
                        INSERT INTO film_directors (film_id, director_id)
                        SELECT :film_id, :director_id
                        WHERE NOT EXISTS(SELECT 1 FROM film_directors WHERE film_id = :film_id 
                                                            AND director_id = :director_id)"""
                cur.execute(query, {"film_id": k.id, "director_id": item.get('id')})
    con.commit()




def actors_to_film(df,con):
    cur = con.cursor()
    for i, k in df[['id', 'actors']].iterrows():
        if k.actors:
            for item in tqdm(k.actors):
                query = """
                        INSERT INTO film_actors (film_id, actor_id)
                        SELECT :film_id, :actor_id
                        WHERE NOT EXISTS(SELECT 1 FROM film_actors WHERE film_id = :film_id 
                                                            AND actor_id = :actor_id)"""
                cur.execute(query, {"film_id": k.id, "actor_id": item.get('id')})
    con.commit()


def genres_to_film(df,con):
    cur = con.cursor()
    for i, k in tqdm(df[['id', 'genres']].iterrows()):
        if k.genres:
            for item in k.genres:
                query = """
                        INSERT INTO film_genres (film_id, genr_id)
                        SELECT :film_id, :genr_id
                        WHERE NOT EXISTS(SELECT 1 FROM film_genres WHERE film_id = :film_id 
                                                            AND genr_id = :genr_id)"""
                cur.execute(query, {"film_id": k.id, "genr_id": item.get('id')})
    con.commit()




def add_poster(df,con):
    cur = con.cursor()
    for i, k in tqdm(df[['id', 'poster']].iterrows()):
        if k.poster:
            params = {'film_id': k.id,
                      'poster_rgb': k.poster.get('rgb'),
                      'poster_name': k.poster.get('name')}
            query = """
                INSERT INTO poster_film (film_id, poster_rgb, poster_name)
                SELECT :film_id, :poster_rgb, :poster_name
                WHERE NOT EXISTS
                (SELECT 1 FROM poster_film  WHERE film_id = :film_id)"""
            cur.execute(query, params)
    con.commit()



def add_posterLandscape(df,con):
    cur = con.cursor()
    for i, k in tqdm(df[['id', 'posterLandscape']].iterrows()):
        if k.posterLandscape:
            params = {'film_id': k.id,
                      'posterLandscape_rgb': k.posterLandscape.get('rgb'),
                      'posterLandscape_name': k.posterLandscape.get('name')}
            query = """
                INSERT INTO posterLandscape_film (film_id, posterLandscape_rgb, posterLandscape_name)
                SELECT :film_id, :posterLandscape_rgb, :posterLandscape_name
                WHERE NOT EXISTS
                (SELECT 1 FROM posterLandscape_film  WHERE film_id = :film_id)"""
            cur.execute(query, params)
    con.commit()



def add_images_film(df,con):
    cur = con.cursor()
    for i, k in tqdm(df[['id', 'images']].iterrows()):
        if k.images:
            for item in k.images:
                params = {"film_id": k.id,
                          "rgb": item.get("rgb"),
                          "name": item.get("name")}
                query = """
                INSERT INTO film_images (film_id, rgb, name)
                SELECT :film_id, :rgb, :name
                WHERE NOT EXISTS
                (SELECT 1 FROM film_images  WHERE film_id = :film_id and name = :name)"""
                cur.execute(query, params)
    con.commit()



def add_trailers_previws(df,con):
    cur = con.cursor()
    for i, k in tqdm(df[['id','trailers']].iterrows()):
        if k.trailers:
            for item in k.trailers:
                params = {"film_id": k.id,
                          "name": item.get('preview').get('name'),
                          "rgb": item.get('preview').get('rgb')}
                query = """
                INSERT INTO film_trailers_previews (film_id, rgb, name)
                SELECT :film_id, :rgb, :name
                WHERE NOT EXISTS
                (SELECT 1 FROM film_trailers_previews  WHERE film_id = :film_id and name = :name)"""
                cur.execute(query, params)
    con.commit()



def add_videoinfo_source(df,con):
    cur = con.cursor()
    for i, k in tqdm(df[['id','trailers']].iterrows()):
        if k.trailers:
            for item in k.trailers:
                params = {"film_id": k.id,
                          "filename": item.get('source').get('filename'),
                          "contentType": item.get('source').get('contentType'),
                          "duration": item.get('source').get('duration')}
                query = """
                INSERT INTO film_trailers_sources (film_id, filename, contentType, duration)
                SELECT :film_id, :filename, :contentType, :duration
                WHERE NOT EXISTS
                (SELECT 1 FROM film_trailers_sources  WHERE film_id = :film_id and filename = :filename)"""
                cur.execute(query, params)
    con.commit()


def add_trailers_video(df,con):
    cur = con.cursor()
    for i, k in tqdm(df[['id','trailers']].iterrows()):
        if k.trailers:
            for item in k.trailers:
                if item.get('videos'):
                    for video in item.get('videos'):
                        params = {"film_id": k.id,
                                  "filename": video.get('filename'),
                                  "contentType": video.get('contentType'),
                                  "duration": video.get('duration')}
                        query = """
                        INSERT INTO film_trailers_videos (film_id, filename, contentType, duration)
                        SELECT :film_id, :filename, :contentType, :duration
                        WHERE NOT EXISTS
                        (SELECT 1 FROM film_trailers_sources  WHERE film_id = :film_id and filename = :filename)"""
                        cur.execute(query, params)
    con.commit()


def add_format_to_seance(df, con):
    cur = con.cursor()
    for i, k in tqdm(df[['id', 'formats']].iterrows()):
        if k.formats:
            for f in k.formats:
                query = """
                INSERT INTO seances_format (seance_id, format)
                SELECT :seance_id, :format
                WHERE NOT EXISTS
                (SELECT 1 FROM seances_format WHERE seance_id = :seance_id AND format = :format)"""
                cur.execute(query, {"seance_id": k.id, "format": f})
    con.commit()



def full_languages(df, conn):
    cur = conn.cursor()
    for i , k in tqdm(df.iterrows()):
        params = {"id_lang": k.id,
                  "title": k.title,
                  "prepTitle": k.prepTitle,
                  "origTitle": k.origTitle,
                  "shortTitle": k.shortTitle,
                  "greeting": k.greeting}
        query = """
            INSERT INTO languages
            (id_lang, title, prepTitle, origTitle, shortTitle, greeting)
            SELECT :id_lang, :title, :prepTitle, :origTitle, :shortTitle, :greeting
            WHERE NOT EXISTS
            (SELECT 1 FROM languages WHERE id_lang = :id_lang)"""
        cur.execute(query, params)
    conn.commit()



def update_film(df, con):
    cur = con.cursor()
    for i, k in df.iterrows():
        params = {'movieid': k.id,
                  'title': k.title,
                  'originalTitle': k.originalTitle,
                  'duration': k.duration,
                  'productionYear': k.productionYear,
                  'premiereDateRussia': k.premiereDateRussia,
                  'premiereDateWorld': k.premiereDateWorld,
                  'budget': k.budget,
                  'annotationShort': k.annotationShort,
                  'annotationFull': k.annotationFull,
                  'ageRestriction': k.ageRestriction,
                  'grossRevenueRus': k.grossRevenueRus,
                  'grossRevenueWorld': k.grossRevenueWorld,
                  'rating': k.rating,
                  'imdbId': k.imdbId,
                  'externalTrailer': k.externalTrailer,
                  'countScreens': k.countScreens,
                  'countVotes': k.countVotes,
                  'countComments': k.countComments,
                  'weight': k.weight,
                  'isDolbyAtmos': k.isDolbyAtmos,
                  'isImax': k.isImax,
                  'is4dx': k.is4dx,
                  'isPresale': k.isPresale,
                  'distributorId': k.distributorId}
        query = """
                    INSERT INTO films (movieid,title,originalTitle,duration,
                            productionYear,premiereDateRussia,premiereDateWorld,
                            budget,annotationShort,annotationFull,ageRestriction,
                            grossRevenueRus,grossRevenueWorld,rating,imdbId,
                            externalTrailer,countScreens,countVotes,
                            countComments,weight,isDolbyAtmos,isImax,
                            is4dx,isPresale,distributorId)
                    SELECT  :movieid,:title,:originalTitle,:duration,
                            :productionYear,:premiereDateRussia,:premiereDateWorld,
                            :budget,:annotationShort,:annotationFull,:ageRestriction,
                            :grossRevenueRus,:grossRevenueWorld,:rating,:imdbId,
                            :externalTrailer,:countScreens,:countVotes,
                            :countComments,:weight,:isDolbyAtmos,
                            :isImax,:is4dx,:isPresale,:distributorId
                            WHERE NOT EXISTS(SELECT 1 FROM films WHERE movieid = :movieid)"""
        cur.execute(query, params)
    conn.commit()


def get_all_cities(con):
    query = """
    SELECT cityid from cities"""
    a = pd.read_sql(query, con)
    return a.cityid.values



if __name__ == '__main__':
    conn = utils.connection(utils.DB_ROOT)
    create_table(utils.filmps_params, 'films', conn)
    create_table(utils.cinema_params, 'cinemas', conn)
    create_table(utils.cities_params, 'cities', conn)
    create_table(utils.halls_params, 'halls', conn)
    create_table(utils.seances_params, 'seances', conn)
    df_lang = create_df_with_data('../data/languages.json')
    #print(df_lang.head(20))
    #full_languages(df_lang,conn)
    #df_film = create_df_with_data('../data/all_films.json')
    #add_producers(df_film,conn
    #add_companies(df_film, conn)
    #add_directors(df_film, conn)
    #add_genres(df_film, conn)
    #add_actors(df_film, conn)
    #country_for_film(df_film, conn)
    #df_cities = create_df_with_data('../data/cities.json')
    #df_halls = create_df_with_data('../data/halls.json')
    #df_seances = create_df_with_data('../data/seances.json')
    #df_cinemas = create_df_with_data('../data/cinemas.json')
    #print(df_film.trailers.head())
    #add_format_to_seance(df_seances, conn)
    #add_images_film(df_film,conn)
    #producer_for_film(df_film,conn)
    #companies_to_film(df_film,conn)
    #directors_to_film(df_film,conn)
    #actors_to_film(df_film, conn)
    #genres_to_film(df_film,conn)
    #add_phones(df_cinemas,conn)
    #add_goodies(df_cinemas, conn)
    #full_films(df_film, conn)
    #full_cinema(df_cinemas, conn)
    #full_cities(df_cities, conn)
    #full_halls(df_halls, conn)
    #full_seances(df_seances, conn)
    #b = get_report(CITIES)
    #print(b[['id']].head())
    #full_cities(b, conn)
    #update_film(a, conn)
    get_report_for_all_cities(SEANCES_SOON, conn)

