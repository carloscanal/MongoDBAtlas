#!/usr/bin/python

# Copyright (c) 2017 ObjectLabs Corporation
# Distributed under the MIT license - http://opensource.org/licenses/MIT

__author__ = 'mLab'

# Written with pymongo-3.4
# Documentation: http://docs.mongodb.org/ecosystem/drivers/python/
# A python script connecting to a MongoDB given a MongoDB Connection URI.

import sys
import pymongo
from environs import Env

### Get database URI from the .env file: 

env = Env()
env.read_env()  # read .env file, if it exists

uri = env('MONGO_URI')      # establecer la variable de entorno MONGO_URI con la URI de la base de datos
                            # MongoDB local:
                            #   MONGO_URI = mongodb://localhost:27017
                            # MongoDB Atlas:
                            #   MONGO_URI = mongodb+srv://<USER>:<PASS>@<CLUSTER>.mongodb.net/<DB>?retryWrites=true&w=majority
                            # MongoDB en Docker
                            #   MONGO_URI = mongodb://root:example@mongodb:27017

print("MONGO_URI: ",uri)

### Create seed data

SEED_DATA = [
    {
        'decade': '1970s',
        'artist': 'Debby Boone',
        'song': 'You Light Up My Life',
        'weeksAtOne': 10
    },
    {
        'decade': '1980s',
        'artist': 'Olivia Newton-John',
        'song': 'Physical',
        'weeksAtOne': 10
    },
    {
        'decade': '1990s',
        'artist': 'Mariah Carey',
        'song': 'One Sweet Day',
        'weeksAtOne': 16
    }
]

###############################################################################
# main
###############################################################################

def main(args):

    client = pymongo.MongoClient(uri)

    db = client.iweb    # db = client['iweb']
                        # db = client.get_default_database()    # da error si no hay DB por defecto en el cluster
    
    # First we'll add a few songs. Nothing is required to create the songs 
    # collection; it is created automatically when we insert.

    songs = db.songs    # songs = db['songs']

    # Note that the insert method can take either an array or a single dict.

    songs.insert_many(SEED_DATA)

    # Then we need to give Boyz II Men credit for their contribution to
    # the hit "One Sweet Day".

    query = {'song': 'One Sweet Day'}

    songs.update_many(query, {'$set': {'artist': 'Mariah Carey ft. Boyz II Men'}})

    # Finally we run a query which returns all the hits that spent 10 or
    # more weeks at number 1.

    cursor = songs.find({'weeksAtOne': {'$gte': 10}}).sort('decade', 1)

    for doc in cursor:
        print ('In the %s, %s by %s topped the charts for %d straight weeks.' %
               (doc['decade'], doc['song'], doc['artist'], doc['weeksAtOne']))
    
    ### Since this is an example, we'll clean up after ourselves.

    # db.drop_collection('songs')

    ### Only close the connection when your app is terminating

    client.close()


if __name__ == '__main__':
    main(sys.argv[1:])
