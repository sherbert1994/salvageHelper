# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 15:53:31 2025

@author: feysn
"""

def get_craft_info():
    min_batch = input("What's minimum amount of items you want to craft per item: ")
    try:
        min_batch = int(min_batch)
    except:
        min_batch = 10
        
    min_profit = input("What's minimum profit per craft you want: ")
    try:
        min_profit = int(min_profit)
    except:
        min_profit = 100
        
    max_gold = input("What's the maximum amount of gold you want to spend: ")
    try:
        max_gold = int(max_gold) * 100 * 100
    except:
        max_gold = 1000 * 100 * 100
        
    weekly_saturation = input("How much % of the weekly market do you want to craft: ")
    try:
        weekly_saturation = float(weekly_saturation) / 100
        if weekly_saturation < 0 or weekly_saturation > 1:
            weekly_saturation = 0.25
    except:
        weekly_saturation = 0.25
        
    
    