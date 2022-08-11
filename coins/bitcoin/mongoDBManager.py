from pymongo import MongoClient


class setimentalResult(object):
    def __init__(self):
        client = MongoClient("117.17.189.6", 27017)
        self.db = client['tweet']
        self.collection = self.db.kafka_tweet_2

    def get_users_from_collection(self):
        # doc=self.collection.find({})
        doc= self.collection.find({"created_at": {'$regex': "Mon"}})
        return doc

