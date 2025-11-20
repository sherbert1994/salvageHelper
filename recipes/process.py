# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 13:47:25 2025

@author: feysn
"""

import db.database
from recipes.recipe import Recipe
import items.tradingpost as tp

sellable_items = tp.item_prices
sellable_items_list = sellable_items["id"].tolist()

def make_recipe_dict(recipe_list):
    recipe_dict = {}
    for r in recipe_list:
        recipe_dict[r.recipe_id] = r
        
    return recipe_dict

def make_recipe_list():
    recipe_list = []
    query = """
        SELECT * FROM recipes WHERE other = 0
    """
    
    try:
        conn = db.database.get_connection()
        cursor = conn.cursor()
        recipes = cursor.execute(query)
        
        for r in recipes:
            if r[1] in sellable_items_list:
                recipe_list.append(Recipe(r))
    finally:
        conn.close()
    return recipe_list

def calc_profit(recipe_dict):
    for index, r in recipe_dict.items():
        r.get_profit(recipe_dict)


if __name__ == "__main__":
    dic = make_recipe_dict(make_recipe_list())
    calc_profit(dic)
    
    profit = lambda r : r.profit 
    
    result = list(dic.values())
    sorted_result = sorted(result, key=profit, reverse=True)
    pass
    