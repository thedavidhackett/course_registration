import pymongo
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from sqlalchemy import create_engine, Engine

#main database
db : Engine = create_engine("mysql+pymysql://course_registration:course_registration@mysql-db:3306/course_registration")

#notifications database
client : MongoClient = MongoClient(host='mongo',port=27017, username='root',password='pass', authSource="admin")
mongo_db : Database = client.notification_db
notifications : Collection = mongo_db.notification
