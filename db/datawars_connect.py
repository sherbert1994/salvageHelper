# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 14:21:39 2025

@author: feysn
"""

import requests
import pandas as pd
from db.database import get_known_ids, push_to_database
import math

BASE_URL = "https://api.datawars2.ie/gw2/"


def update_recipes():
    url = BASE_URL + "v2/recipes?filter=id"
    response = requests.get(url)
    recipes = pd.json_normalize(response.json())
    known_ids = get_known_ids("recipes")
    params_list = []
    
    param_query = """
        INSERT INTO recipes
        (recipe_id, output_id, output_count, item_1_id, item_1_count,
         item_2_id, item_2_count, item_3_id, item_3_count,
         item_4_id, item_4_count, item_5_id, item_5_count,
         artificer, armorsmith, chef, homesteader, huntsman, jeweler,
         leatherworker, tailor, weaponsmith, scribe, other)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    recipes = recipes[~recipes["id"].isin(known_ids)]
    
    recipes_to_update = recipes.shape[0]
    
    for recipe in recipes.itertuples():
        index = recipe[0]
        params = []
        params.append(recipe[1])
        params.append(recipe[10])
        params.append(recipe[9])
        ingredients = recipe[6]
        if len(ingredients) > 5:
            max_loops = 5
            print(f"recipe_id:{recipe[1]}{ingredients}")
        else:
            max_loops = len(ingredients)
            
        for i in range(max_loops):
            params.append(ingredients[i].get("item_id"))
            params.append(ingredients[i].get("count"))
        for i in range(max_loops, 5):
            params.append(None)
            params.append(None)
        disciplines = recipe[3]
        disciplines_bools = []
        disciplines_list = ["Artificer", "Armorsmith", "Chef", "Homesteader", "Huntsman", "Jeweler", "Leatherworker", "Tailor", "Weaponsmith", "Scribe"]
        
        for d in disciplines_list:
            if d in disciplines:
                disciplines_bools.append(True)
            else:
                disciplines_bools.append(False)
        if True in disciplines_bools:
            disciplines_bools.append(False)
        else:
            disciplines_bools.append(True)
        
        params.extend(disciplines_bools)
    
        params_list.append(tuple(params))
        
        if index % 100 == 0:
            print(f"Finished iteration {math.floor(recipe[0]/100)} of {math.floor(recipes_to_update / 100) + 1}")
        
    push_to_database(param_query, params_list)
    
    

if __name__ == "__main__":
    update_recipes()