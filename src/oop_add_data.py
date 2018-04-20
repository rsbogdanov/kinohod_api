from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src import oop_work_with_api

from src.oop_test import Base, Distributors

engine = create_engine('sqlite:///../data/oop_test2.db', encoding='utf-8')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
session = DBSession()

a = oop_work_with_api.ApiKinohod('https://api.kinohod.ru/api/data/2/5982bb5a-1d76-31f8-abd5-c4253474ecf3/')
df = a.get_json()


# from src.utils import connection
# import pandas as pd
# conn = connection('../data/oop_test2.db')
# query = "SELECT distributors from distributors"
# df2 = pd.read_sql(query,conn)
# print(df2.head())

#
if __name__ == '__main__':
    for k,v in df.iterrows():
        new_destr = Distributors(distributors=v['name'])
        print(v['id'], type(v['name']))
        session.add(new_destr)
        session.commit()

# for k,v in df[:5].iterrows():
#     print(v['id'], v['name'])