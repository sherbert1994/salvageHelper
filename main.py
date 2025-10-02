# -*- coding: utf-8 -*-
"""
Created on Wed Oct  1 19:43:31 2025

@author: feysn
"""

from db import database, api_connect
from items import process



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
   
#list of items that have the requirements to salvage for profit
itemlist = process.make_itemlist()

#sorting keys
buy = lambda item: item.buy_profit
sell = lambda item: item.sell_profit


itemlist.sort(key=sell, reverse=True)
for item in itemlist:
    print(f"{item.name:<50} {item.value:>20}")
    
    