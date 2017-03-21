
import datetime
import pymongo

from settings import MONGODB_SETTINGS


class MongoClientManager(object):
    """
        Singleton for accessing mongo client
    Attributes:
        None
    """
    class __MongoClientManager(object):
        def __init__(self):
            if "username" in MONGODB_SETTINGS and "password" in MONGODB_SETTINGS:
                self.client = pymongo.MongoClient('mongodb://%s:%s@%s' % (MONGODB_SETTINGS["username"], MONGODB_SETTINGS["password"], MONGODB_SETTINGS["host"]), maxPoolSize=200, connect=False)
            else:
                self.client = pymongo.MongoClient('mongodb://%s' % (MONGODB_SETTINGS["host"]), maxPoolSize=200, connect=False)

    __instance = None

    def __new__(cls):
        """
            Constructor checking for a single instance
        Attributes:
            None
        """
        if not MongoClientManager.__instance:
            MongoClientManager.__instance = MongoClientManager.__MongoClientManager()
        return MongoClientManager.__instance

    def __getattr__(self, name):
        return getattr(self.__instance, name)


def get_connection():
    """
        Method for retrieving a MongoClient according to the environment we are running on
    Attributes:
        None
    """

    return MongoClientManager().client.__getattr__(MONGODB_SETTINGS['db'])


def get_client():
    """
        Method for retrieving a MongoClient according to the environment we are running on
    Attributes:
        None
    """

    return MongoClientManager().client
