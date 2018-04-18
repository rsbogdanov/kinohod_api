import sqlite3

DB_ROOT = 'D:/kinohod_db/kinohod.db'

def connection(db_root):
    with sqlite3.connect(db_root) as con:
        return con



cinema_params = """
                'cinema_id' INEGER,
                'title' TEXT,
                'shortTitle' TEXT,
                'description' TEXT,
                'website' TEXT,
                'cityId' INTEGER,
                'address' TEXT,
                'location' TEXT,
                'networkId' INTEGER,
                'isSale' NUMERIC,
                'mall' TEXT,
                'timeToRefund' INTEGER,
                'hallCount' INTEGER,
                PRIMARY KEY('cinema_id')"""


cities_params = """
                'cityid' INTEGER,
                'title' TEXT,
                'location' TEXT,
                'utcOffset' INTEGER,
                'alias' TEXT,
                PRIMARY KEY(`cityid`)"""


filmps_params = """
                `movieid` INTEGER ,
                `title` TEXT,
                `originalTitle` TEXT,
                `duration` INTEGER,
                `productionYear` INTEGER,
                `premiereDateRussia` TEXT,
                `premiereDateWorld` TEXT,
                `budget` NUMERIC,
                `annotationShort` TEXT,
                `annotationFull` TEXT,
                `ageRestriction` TEXT,
                `grossRevenueRus` NUMERIC,
                `grossRevenueWorld` NUMERIC,
                `rating` NUMERIC,
                'imdbId' TEXT,
                'externalTrailer' STRING,
                'countScreens' INTEGER,
                'countVotes' INTEGER,
                'countComments' INTEGER,
                'weight' INTEGER,
                'isDolbyAtmos' NUMERIC,
                'isImax' NUMERIC,
                'is4dx' NUMERIC,
                'isPresale' NUMERIC,
                'distributorId' INTEGER,
                PRIMARY KEY(`movieid`)"""


halls_params = """
                'hall_id' INTEGER,
                'cinemaId' INTEGER,
                'title' TEXT,
                'description' TEXT,
                'placeCount' INTEGER,
                'isVIP' NUMERIC,
                'isIMAX' NUMERIC,
                'orderScanner' NUMERIC,
                'ticketScanner' NUMERIC,
                PRIMARY KEY('hall_id')"""


seances_params = """
                `seanc_id` INTEGER,
                `movieId` INTEGER,
                `cinemaId` INTEGER,
                `date` TEXT,
                `time` TEXT,
                `startTime` TEXT,
                `hallId` INTEGER,
                `isSaleAllowed` NUMERIC,
                `minPrice` NUMERIC,
                `maxPrice` NUMERIC,
                `maxSeatsInOrder` INTEGER,
                `subtitleId` INTEGER,
                `languageId` INTEGER,
                `groupName` TEXT,
                `groupOrder` INTEGER,
                PRIMARY KEY(`seanc_id`)"""



"""
cur.execute("drop table cities")
con.commit()"""