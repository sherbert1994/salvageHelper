# -*- coding: utf-8 -*-
"""
Created on Wed Oct  1 19:43:31 2025

@author: feysn
"""

from db import database, api_connect, datawars_connect
import salvage
import craft

#create the database if it does not yet exist
database.create()
    
#update the itemstats table of the database if there is new data to be added
api_connect.update_itemstats()
    
"""
update the items table of the database if there is new data to be added
first time filling this table will take a while as speed partially depends
on how fast the gw2 api can answer the requests
"""
api_connect.update_items()

print("updating recipes")
datawars_connect.update_recipes()

options = ["salvage", "craft"]

choice = input("Pick an option: salvage or craft: ").lower()

if choice not in options:
    print("Invalid choice, defaulting to salvage. ")
    choice = "salvage"

if choice == "salvage":
    salvage.get_salvage_stats()
elif choice == "craft":
    craft.get_craft_info()
    