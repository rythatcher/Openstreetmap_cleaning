# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 13:08:21 2015

@author: Ryan
"""

import pymongo as pm
import OSM_to_JSON as oj

client = pm.MongoClient('mongodb://localhost:27017')
db = client.udacity

def insert_data(infile, db):
    data = oj.process_map(infile, False)
    for x in data:
        db.syracuse.insert(x)
    
insert_data('C:/Users/Ryan/Desktop/Project_3_OSM/syracuse_new-york.osm', db)