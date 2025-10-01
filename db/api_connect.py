# -*- coding: utf-8 -*-
"""
Created on Wed Oct  1 14:47:33 2025

@author: feysn
"""

import requests
from db import database
import math

BASE_URL = "https://api.guildwars2.com/v2/"

def get_itemstats_ids() -> list[int]:
    url = BASE_URL + "itemstats"
    response = requests.get(url)
    ids = []
    
    if response.status_code == 200:
        ids = response.json()
    else:
        print("Something is wrong with the Guild Wars 2 API, please try again in an hour")
        print("Continuing without updating data...")
        
    return ids

def get_itemstats_data(ids : list[int]) -> list[dict]:
    itemstats_data = []
    if len(ids)>100:
        raise ValueError("Too many ids in the list")
    
    params = ",".join(map(str,ids))
    url = BASE_URL + "itemstats?ids=" + params
    
    response = requests.get(url)

    if response.status_code == 200:
        itemstats_data = response.json()
    else:
        print("Something is wrong with the Guild Wars 2 API, please try again in an hour")
        print("Skipping these itemstats...")
    
    return itemstats_data

def update_itemstats():
    BATCH_SIZE = 100 #max amount of ids we can request in one go
    itemstats_ids = get_itemstats_ids() # all itemstats ids that are exposed by the GW2 API
    known_itemstats_ids = database.get_known_itemstats_ids()
    ids_to_fetch = __difference(itemstats_ids, known_itemstats_ids)
    
    param_query = """
        INSERT INTO itemstats VALUES (?, ?)
    """
    
    print(f"Found {len(ids_to_fetch)} new itemstats")
    
    
    for i in range(0, len(ids_to_fetch), BATCH_SIZE):
        iterations = math.ceil(len(ids_to_fetch)/100)
        itemstats = get_itemstats_data(ids_to_fetch[i:i+BATCH_SIZE])
        
        for itemstat in itemstats:
            params = [None, None]
            params[0] = itemstat["id"]
            params[1] = itemstat["name"]
            database.push_to_database(param_query, tuple(params))
            
        print(f"Finished iteration {int((i/100) + 1)} out of {iterations}")
    
def get_item_ids() -> list[int]:
    url = BASE_URL + "items"
    response = requests.get(url)
    ids = []
    
    if response.status_code == 200:
        ids = response.json()
    else:
        print("Something is wrong with the Guild Wars 2 API, please try again in an hour")
        print("Continuing without updating data...")
        
    return ids

def get_items_data(ids: list[int]) -> list[dict]:
    items_data = []
    if len(ids)>100:
        raise ValueError("Too many ids in the list")
        
    params = ",".join(map(str,ids))
    url = BASE_URL + "items?ids=" + params
    
    response = requests.get(url)
    
    if response.status_code == 200:
        items_data = response.json()
    else:
        print("Something is wrong with the Guild Wars 2 API, please try again in an hour")
        print("Skipping these items...")
    
    return items_data
     
def update_items():
    BATCH_SIZE = 100
    items_ids = get_item_ids() # all item ids that are exposed by the GW2 API
    known_items_ids = database.get_known_items_ids()
    ids_to_fetch = __difference(items_ids, known_items_ids)
    
    param_query = """
        INSERT INTO items (item_id, name, description, type, rarity, level, detailed_type, weight, upgrade_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    print(f"Found {len(ids_to_fetch)} new items")
    
    for i in range(0, len(ids_to_fetch), BATCH_SIZE):
        iterations = math.ceil(len(ids_to_fetch)/100)
        items = get_items_data(ids_to_fetch[i:i+BATCH_SIZE])
        
        for item in items:
            params = []
            params.append(item.get("id"))
            params.append(item.get("name"))
            params.append(item.get("description"))
            params.append(item.get("type"))
            params.append(item.get("rarity"))
            params.append(item.get("level"))
            detailsObject = item.get("details")
            if detailsObject is not None:
                params.append(detailsObject.get("type"))
                params.append(detailsObject.get("weight_class"))
                params.append(detailsObject.get("suffix_item_id"))
            else:
                params.extend([None]*3)
            
            print(tuple(params))
            
            database.push_to_database(param_query, tuple(params))
        
        print(f"Finished iteration {int((i/100) + 1)} out of {iterations}")   

def __difference(all_ids: list[int], known_ids: list[int]) -> list[int]:
    all_ids = set(all_ids)
    known_ids = set(known_ids)
    
    return list(all_ids.difference(known_ids))
