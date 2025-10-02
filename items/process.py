# -*- coding: utf-8 -*-
"""
Created on Thu Oct  2 15:23:56 2025

@author: feysn
"""
from items import items
import db.database
import sqlite3
import items.tradingpost as tp


#TODO: add support for armor, trinkets and backpacks
def make_itemlist() -> list[items.Item]:   
    itemlist = []
    try:
        conn = db.database.get_connection()
        cursor = conn.cursor()
        itemlist.extend(get_weapons(cursor))
    finally:
        conn.close()
    return itemlist
        
    
def get_weapons(cursor: sqlite3.Cursor) -> list[items.Weapon]:
    sellable_items = tp.item_prices
    sellable_items_list = sellable_items["id"].tolist()
    
    weaponlist = []
    query = """
        SELECT item_id, items.name, description, level, 
        detailed_type, upgrade_id, itemstats.name
        FROM items
            LEFT OUTER JOIN itemstats USING (itemstat_id)
        WHERE type == "Weapon"
            AND rarity == "Exotic"
            AND level >= 68
    """
    
    weapons = cursor.execute(query)
    for weapon in weapons:
        if weapon[0] in sellable_items_list:
            weaponlist.append(items.Weapon(weapon))            
            
    return weaponlist
        

if __name__ == "__main__":
   itemlist = make_itemlist()
   buy = lambda item: item.buy_profit
   sell = lambda item: item.sell_profit
   itemlist.sort(key=sell)
   for item in itemlist:
       print(item.name)