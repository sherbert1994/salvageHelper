# -*- coding: utf-8 -*-
"""
Created on Thu Oct  2 15:23:56 2025

@author: feysn
"""
from items import items
import db.database
import items.tradingpost as tp

sellable_items = tp.item_prices
sellable_items_list = sellable_items["id"].tolist()


def make_itemlist(salvageKit):   
    itemlist = []
    try:
        conn = db.database.get_connection()
        cursor = conn.cursor()
        itemlist.extend(__get_items(cursor, salvageKit, "Weapon"))
        itemlist.extend(__get_items(cursor, salvageKit, "Armor"))
        itemlist.extend(__get_items(cursor, salvageKit, "Trinket"))
        itemlist.extend(__get_items(cursor, salvageKit, "Back"))
    finally:
        conn.close()
    return itemlist

def __get_items(cursor, salvageKit, itemtype):
    query = """
        SELECT item_id, items.name, description, level, 
        detailed_type, upgrade_id, itemstats.name, weight
        FROM items
            LEFT OUTER JOIN itemstats USING (itemstat_id)
        WHERE type == ?
            AND rarity == "Exotic"
            AND level >= 68
    """
    
    items = cursor.execute(query,(itemtype,))
    if itemtype == "Weapon":
        return __get_weapons(items, salvageKit)
    elif itemtype == "Armor":
        return __get_armors(items, salvageKit)
    elif itemtype == "Trinket" or itemtype == "Back":
        return __get_generic_items(items, salvageKit)
 
        
    
def __get_weapons(weapons, salvageKit):
    weaponlist = []
    
    for weapon in weapons:
        if weapon[0] in sellable_items_list:
            weaponlist.append(items.Weapon(weapon, salvageKit))    
            
    return weaponlist


def __get_armors(armors, salvageKit):
    armorlist = []

    for armor in armors:
        if armor[0] in sellable_items_list:
            armorlist.append(items.Armor(armor, salvageKit))
            
    return armorlist
        

def __get_generic_items(items, salvageKit):
    itemlist = []

    for item in itemlist:
        if item[0] in sellable_items_list:
            itemlist.append(items.Item(item, salvageKit))
    
    return itemlist