import sqlite3
import os

#Manages connection to the databases for easy modifiability of name, location etc. Working with the databases can 
#then be done locally (otherwise every action has to be presented here as a function)


#Establish connections to the databases, openDB()[0]= connection to the monsterDB, openDB()[1] to the itemDB
def openDB():

    #ABSOLUTE filepaths are important or the databases are not found!
    path = os.path.abspath(__file__)

    path = path[:path.rfind(os.sep) + 1]
    #print(path)

    monsterdb = sqlite3.connect(path + '../data/monsters.db')
    itemdb = sqlite3.connect(path + '../data/items.db')
    
    return monsterdb, itemdb
    

#get cursor of an already opened databse
def get_Cursor(db):
	
	return db.cursor()

#close connection to a databse
def closeDB(db):
	
	db.close();
