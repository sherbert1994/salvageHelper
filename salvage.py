# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 14:21:39 2025

@author: feysn
"""
from items import process
import time
import csv

def export_to_csv(itemList, instantbuy):
    column_names = get_column_names(instantbuy)
    with open("salvageData.csv", "w", newline="") as file:
        csvWriter = csv.writer(file)
        csvWriter.writerow(column_names)
        
        for item in itemList:
            if instantbuy == "Y":
                csvWriter.writerow([item.name, round(item.value)])
            else:
                csvWriter.writerow([item.name, item.buy_price])

def print_to_terminal(itemlist, instantbuy):
    column_names = get_column_names(instantbuy)
    print(f"\n{column_names[0]:<50}{column_names[1]:>20}\n")
    
    for item in itemlist[:50]:
        if instantbuy == "Y":
            print(f"{item.name:_<50}{item.value:_>20.0f}")
        else:
            print(f"{item.name:_<50}{item.buy_price:_>20.0f}")
        
def get_column_names(instantbuy):
    name = "ITEM NAME"
    if instantbuy == "Y":
        price = "MAX PRICE"
    else:
        price = "CURRENT PRICE"
    return (name, price)

def get_salvage_stats():
    """
    input for type of salvage kit
    SF: Silver-Fed salvage-o-matic
    BLSK: Black Lion Salvage Kit
    on incorrect input we default to SF
    """
    salvageKit = input("What salvage kit are you using? (SF/BLSK): ").upper().strip()
    if salvageKit not in ["SF", "BLSK"]:
        print("Wrong input, defaulting to Silver-Fed salvage-o-matic (SF)")
        salvageKit = "SF"
       
    #list of items that have the requirements to salvage for profit
    itemlist = process.make_itemlist(salvageKit)
    
    #sorting keys
    buy = lambda item: item.buy_profit * item.bought_7d
    sell = lambda item: item.sell_profit
    
    
    #determine sort order, either profit from instantbuy or profit from buy offer
    instantbuy = input("Are you instant buying (Y: instantbuy/ N: offer)? [Y/N]: ").upper().strip()
    if instantbuy == "Y":
        itemlist.sort(key=sell, reverse=True)
    elif instantbuy == "N":
        itemlist.sort(key=buy, reverse=True)
    else:
        print("Wrong input, defaulting to instantbuy")
        instantbuy = "Y"
        itemlist.sort(key=sell, reverse=True)
    
    
    export = input("Export to csv? [Y/N]: ").upper().strip()
    if export == "Y":
        export_to_csv(itemlist, instantbuy)
    elif export == "N":
        print_to_terminal(itemlist, instantbuy)
    else:
        print("Wrong input, defaulting to printing in terminal")
        time.sleep(1)
        print_to_terminal(itemlist, instantbuy)
