# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 13:45:19 2015

@author: Ryan
"""
import pprint as p

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db
    
def get_query():
    # Insert query for db entries, can be found in attached pdf document.
    query = []        
    return query
    

def aggregate(db, query):
    result = db.syracuse.aggregate(query)
    return result
    
    
if __name__ == '__main__':
    db = get_db('udacity')
    query = get_query()
    result = list(aggregate(db, query))
    p.pprint(result)