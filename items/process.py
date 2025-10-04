# -*- coding: utf-8 -*-
"""
Created on Thu Oct  2 15:23:56 2025

@author: feysn
"""
from items import items
import db.database
import sqlite3
import items.tradingpost as tp


def make_itemlist(salvageKit: str) -> list[items.Item]:   
    itemlist = []
    try:
        conn = db.database.get_connection()
        cursor = conn.cursor()
        itemlist.extend(__get_weapons(cursor, salvageKit))
        itemlist.extend(__get_armors(cursor, salvageKit))
        itemlist.extend(__get_trinkets(cursor, salvageKit))
        itemlist.extend(__get_backpacks(cursor, salvageKit))
    finally:
        conn.close()
    return itemlist
        
    
def __get_weapons(cursor: sqlite3.Cursor, salvageKit: str) -> list[items.Weapon]:
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
            weaponlist.append(items.Weapon(weapon, salvageKit))            
            
    return weaponlist


def __get_armors(cursor: sqlite3.Cursor, salvageKit: str) -> list[items.Armor]:
    sellable_items = tp.item_prices
    sellable_items_list = sellable_items["id"].tolist()
    
    armorlist = []
    query = """
        SELECT item_id, items.name, description, level,
        detailed_type, upgrade_id, itemstats.name, weight
        FROM items
            LEFT OUTER JOIN itemstats USING (itemstat_id)
        WHERE type == "Armor"
            AND rarity == "Exotic"
            AND level >= 68
    """
    
    armors = cursor.execute(query)
    for armor in armors:
        if armor[0] in sellable_items_list:
            armorlist.append(items.Armor(armor, salvageKit))
            
    return armorlist
        

def __get_trinkets(cursor: sqlite3.Cursor, salvageKit: str) -> list[items.Trinket]:
    sellable_items = tp.item_prices
    sellable_items_list = sellable_items["id"].tolist()
    
    trinketlist = []
    query = """
        SELECT item_id, items.name, description, level,
        detailed_type, upgrade_id, itemstats.name
        FROM items
            LEFT OUTER JOIN itemstats USING (itemstat_id)
        WHERE type == "Trinket"
            AND rarity == "Exotic"
            AND level >= 68
    """
    
    trinkets = cursor.execute(query)
    for trinket in trinkets:
        if trinket[0] in sellable_items_list:
            trinketlist.append(items.Trinket(trinket, salvageKit))
    
    return trinketlist
    
    
def __get_backpacks(cursor: sqlite3.Cursor, salvageKit: str) -> list[items.Backpack]:
    sellable_items = tp.item_prices
    sellable_items_list = sellable_items["id"].tolist()
    
    backpacklist = []
    query = """
        SELECT item_id, items.name, description, level,
        detailed_type, upgrade_id, itemstats.name
        FROM items
            LEFT OUTER JOIN itemstats USING (itemstat_id)
        WHERE type == "Back"
            AND rarity == "Exotic"
            AND level >= 68
    """
    
    backpacks = cursor.execute(query)
    for backpack in backpacks:
        if backpack[0] in sellable_items_list:
            backpacklist.append(items.Backpack(backpack, salvageKit))
    return backpacklist
    