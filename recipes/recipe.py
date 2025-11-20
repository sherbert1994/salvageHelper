# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 13:34:39 2025

@author: feysn
"""

import items.tradingpost as tp
import math

sellable_items = tp.item_prices
sellable_items_list = sellable_items["id"].tolist()

class Recipe:
    
    disc= ["Artificer", "Armorsmith", "Chef", "Homesteader", "Huntsman", "Jeweler", "Leatherworker", "Tailor", "Weaponsmith", "Scribe", "Other"]
    disciplines = {}
    
    def __init__(self, data: tuple):
        self.ingredients = {}
        self.profit = None
        self.recipe_id = data[0]
        self.output_id = data[1]
        self.output_count = data[2]
        for i in range(3,13,2):
            if data[i] is not None:
                self.ingredients[data[i]] = data[i+1]
        for i in range(11):
            if data[i+13] == 0:
                self.disciplines[self.disc[i]] = False
            else:
                self.disciplines[self.disc[i]] = True
        
        self.weekly_sold = sellable_items.loc[sellable_items["id"] == self.output_id,"7d_sell_sold"].item()
        self.sell_price = sellable_items.loc[sellable_items["id"] == self.output_id,"sell_price"].item()
    
    
    def expand_ingredients(self, full_recipe_dict):
        ingredients_at_start = self.ingredients
        new_ingredients = {}
        old_ingredients = []
        for i in self.ingredients:
            if i in full_recipe_dict:
                sub_ingredients = full_recipe_dict.get(i).ingredients
                
                for s, count in sub_ingredients.items():
                    new_ingredients[s] = count
                
                # remove ingredient that we expanded
                old_ingredients.append(i)
                
        for o in old_ingredients:
            self.ingredients.pop(o)
        
        merged = self.ingredients.copy()
        for k, v in new_ingredients.items():
            merged[k] = merged.get(k, 0) + v
        
        self.ingredients = merged
        
                
        ingredients_at_end = self.ingredients
        if ingredients_at_start != ingredients_at_end:
            self.expand_ingredients(full_recipe_dict)
    
    def get_craft_price(self, full_recipe_dict):
        craft_price = 0
        self.expand_ingredients(full_recipe_dict)
        for ingredient, count in self.ingredients.items():
            if ingredient in sellable_items_list:
                craft_price += count * sellable_items.loc[sellable_items["id"] == ingredient, "buy_price"].iloc[0]
        
        return craft_price
    
    
    def get_profit(self, full_recipe_dict):
        self.profit = math.floor((self.sell_price * 0.85) - self.get_craft_price(full_recipe_dict))
        
    
