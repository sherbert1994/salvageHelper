# -*- coding: utf-8 -*-
"""
Created on Wed Oct  1 14:47:33 2025

@author: feysn
"""

import requests
from db.database import get_known_ids, push_to_database
import math

BASE_URL = "https://api.guildwars2.com/v2/"


def get_ids(endpoint):
    url = BASE_URL + endpoint
    response = requests.get(url)
    ids = []
    
    if response.status_code == 200:
        ids = response.json()
    else:
        print("Something is wrong with the Guild Wars 2 API, please try again in an hour")
        print("Continuing without updating data...")
        
    return ids

def get_json_data(endpoint, ids):
    
    #ids are integers, we need to turn them to string to be able to join them
    params = ",".join(map(str,ids))
    url = BASE_URL + endpoint + "?ids=" + params
    
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Something is wrong with the Guild Wars 2 API, please try again in an hour")
        print("Skipping these itemstats...")
        return []
   
def __get_ids_to_fetch(ENDPOINT):
    all_ids = get_ids(ENDPOINT)
    known_ids = get_known_ids(ENDPOINT)
    ids_to_fetch = __difference(all_ids, known_ids)
    
    return ids_to_fetch

def update_itemstats():
    ENDPOINT = "itemstats"
    ids = __get_ids_to_fetch(ENDPOINT)
    
    BATCH_SIZE = 200
    param_query = """
        INSERT INTO itemstats VALUES (?, ?)
    """
    
    print(f"Found {len(ids)} new {ENDPOINT}")
    params_list = []
    
    for i in range(0, len(ids), BATCH_SIZE):
        iterations = math.ceil(len(ids)/BATCH_SIZE)
        itemstats = get_json_data(ENDPOINT, ids[i:i+BATCH_SIZE])
        
        for itemstat in itemstats:
            params = []
            params.append(itemstat["id"])
            params.append(itemstat["name"])  
        
            params_list.append(params)
        print(f"Finished iteration {int((i/100) + 1)} out of {iterations}")
    
    push_to_database(param_query, params_list)
     
def update_items():
    ENDPOINT = "items"
    ids = __get_ids_to_fetch(ENDPOINT)
    
    BATCH_SIZE = 100
    param_query = """
        INSERT INTO items 
        (item_id, name, description, type, rarity, level, detailed_type, 
         weight, upgrade_id, itemstat_id) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    print(f"Found {len(ids)} new {ENDPOINT}")
    params_list = []
    
    for i in range(0, len(ids), BATCH_SIZE):
        iterations = math.ceil(len(ids)/BATCH_SIZE)
        items = get_json_data(ENDPOINT, ids[i:i+BATCH_SIZE])
        
        for item in items:
            params = []
            params.append(item.get("id"))
            params.append(item.get("name"))
            params.append(item.get("description"))
            params.append(item.get("type"))
            params.append(item.get("rarity"))
            params.append(item.get("level"))
            details_object = item.get("details")
            if details_object is not None:
                params.append(details_object.get("type"))
                params.append(details_object.get("weight_class"))
                params.append(details_object.get("suffix_item_id"))
                itemstat_object = details_object.get("infix_upgrade")
                if itemstat_object is not None:
                    params.append(itemstat_object.get("id"))
                else:
                    params.append(None)
            else:
                params.extend([None]*4)
                
            params_list.append(tuple(params))
        
        print(f"Finished iteration {int((i/100) + 1)} out of {iterations}") 
        
    push_to_database(param_query, params_list)

def __difference(all_ids, known_ids):
    all_ids = set(all_ids)
    known_ids = set(known_ids)
    
    return list(all_ids.difference(known_ids))
