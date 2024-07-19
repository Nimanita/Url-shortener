from pymongo import MongoClient
from django.conf import settings


class MongoConnection(object):
    def __init__(self):
        DATABASES = settings.DATABASES
        self.client = MongoClient(host=[DATABASES['HASHES']['HOST']],
                                  username=DATABASES['HASHES']['USERNAME'],
                                  password=DATABASES['HASHES']['PASSWORD']
                                ,
                                 connect=False)
        self.db = self.client[DATABASES['HASHES']['DATABASE']]


    def get_collection(self, name):
        self.collection = self.db[name]