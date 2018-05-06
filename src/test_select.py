from pymongo import MongoClient
import pandas as pd
import pprint
from datetime import datetime, timedelta


# premiereDateRussia=datetime.strptime(check_is_time(v['premiereDateRussia']),'%Y-%m-%d'),
# premiereDateWorld=datetime.strptime(check_is_time(v['premiereDateWorld']),'%Y-%m-%d'),

client = MongoClient('mongodb://rbogdanov:RomA48917050@localhost:27017/Kinohod')
db = client['Kinohod']

day_x = datetime.today() - timedelta(1)
today = datetime.today()

# for movie in db.movies.find({'premiereDateRussia': {'$gte':today, '$lte':day_x}}):
#     print (movie.get('title'))

a = []

result = db.seanses.delete_one({'startTime': {'$lte': today}})
print(result.deleted_count)

for seance in db.seanses.find({'startTime': {'$lte': today}}):
    a.append(seance.get('id'))
print(len(a))