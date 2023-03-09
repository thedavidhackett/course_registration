import pymongo
from pymongo import MongoClient
from sqlalchemy import create_engine

#main database
db = create_engine("mysql+pymysql://course_registration:course_registration@mysql-db:3306/course_registration")

#notifications database
client = MongoClient(host='mongo',port=27017, username='root',password='pass', authSource="admin")
mongo_db = client.notification_db
notifications = mongo_db.notification
