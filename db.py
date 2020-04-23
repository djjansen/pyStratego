
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017')

db = client.pystratego
collection = db.gameSessions

def createSession(sessionDocument):
	collection.insert_one(sessionDocument)

def fetchOne(query):
	result = collection.find_one(query)
	return result

def updateOne(query,new_values):
	collection.update_one(query,new_values)