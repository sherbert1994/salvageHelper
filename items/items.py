# -*- coding: utf-8 -*-
"""
Created on Thu Oct  2 14:28:45 2025

@author: feysn
"""

from items import tradingpost


class Item():
    ECTO_ID = 19721 #static id for item: Glob of Ectoplasm
    item_prices = tradingpost.item_prices
    ecto_price = item_prices.loc[item_prices["id"] == ECTO_ID,"sell_price"].item()
    
    salvage_cost = {
        "SF": 60,
        "BLSK": 6
        }
    ectos = {
        "SF": 1.2,
        "BLSK": 1.6
        }
    stats_salvage_rate = {
        "SF": 0.4,
        "BLSK": 0.6
        }
    
    
    def __init__(self, data : tuple, salvageKit: str):
        self.item_id = data[0]
        self.name = data[1]
        self.description = data[2]
        self.level = data[3]
        self.salvageKit = salvageKit
        self.buy_price = self.item_prices.loc[self.item_prices["id"] == self.item_id,"buy_price"].iloc[0]
        self.sell_price = self.item_prices.loc[self.item_prices["id"] == self.item_id,"buy_price"].iloc[0]
    
class Armor(Item):
    # maps weapons stats to the insignia salvaged from them
    # only 6 stats have this property
    stats_salvage = {
        "Cavalier's": 46709,
        "Dire": 49522,
        "Magi's": 46711,
        "Rabid": 46710,
        "Shaman's": 46708,
        "Soldier's": 46712
        }
    
    def __init__(self, data: tuple, salvageKit: str):
        super().__init__(data, salvageKit)
        self.detailed_type = data[4]
        self.upgrade_id = data[5]
        self.itemstat = data[6]
        self.weight = data[7]
        self.value = self.get_value()
        
        #profit if item bought at buy_price
        self.buy_profit = self.value - self.buy_price
        #profit if item bought at sell_price (instabuy)
        self.sell_profit = self.value - self.buy_price
        
        
    def get_value(self):
        if self.upgrade_id is not None and self.upgrade_id in self.item_prices["id"].values:
            upgrade_price = self.item_prices.loc[self.item_prices["id"] == self.upgrade_id, "sell_price"].iloc[0]
        else:
            upgrade_price = 0
            
        insignia_id = self.stats_salvage.get(self.itemstat)
        if insignia_id is not None:
            insignia_price = self.item_prices.loc[self.item_prices["id"] == insignia_id, "sell_price"].iloc[0]
        else:
            insignia_price = 0
            
        # amount of ectos * their price + price of the upgrade + avg_inscriptions * their price
        # all multiplied by 0.85 to account for taxes incurred, then the cost of doing a salvage is subtracted
        return (self.ecto_price * self.ectos.get(self.salvageKit) + upgrade_price \
                 + insignia_price * self.stats_salvage_rate.get(self.salvageKit)) * 0.85 \
                 - self.salvage_cost.get(self.salvageKit)

        
class Weapon(Item):
    # maps weapons stats to the inscription salvaged from them
    # only 6 stats have this property
    stats_salvage = {
        "Cavalier's": 46685,
        "Dire": 46690,
        "Magi's": 46687,
        "Rabid": 46686,
        "Shaman's": 46684,
        "Soldier's": 46688
        }
    
    
    def __init__(self, data: tuple, salvageKit: str):
        super().__init__(data, salvageKit)
        self.detailed_type = data[4]
        self.upgrade_id = data[5]
        self.itemstat = data[6]
        self.value = self.get_value()
        
        #profit if item bought at buy_price
        self.buy_profit = self.value - self.buy_price
        #profit if item bought at sell_price (instabuy)
        self.sell_profit = self.value - self.buy_price
        
    """
        Returns the value of an item when we extract and salvage
        (We always do these together as only salvaging is always lower profit)
    """    
    def get_value(self, salvageKit="SF") -> float:
        if self.upgrade_id is not None and self.upgrade_id in self.item_prices["id"].values:
            upgrade_price = self.item_prices.loc[self.item_prices["id"] == self.upgrade_id,"sell_price"].iloc[0]
        else:
            upgrade_price = 0
            
        inscription_id = self.stats_salvage.get(self.itemstat)
        if inscription_id is not None:
            inscription_price = self.item_prices.loc[self.item_prices["id"] == inscription_id, "sell_price"].iloc[0]
        else:
            inscription_price = 0
           
        
        # amount of ectos * their price + price of the upgrade + avg_inscriptions * their price
        # all multiplied by 0.85 to account for taxes incurred, then the cost of doing a salvage is subtracted
        return (self.ecto_price * self.ectos.get(salvageKit) + upgrade_price \
                + inscription_price * self.stats_salvage_rate.get(salvageKit)) * 0.85 \
                - self.salvage_cost.get(salvageKit)
        
        
class Trinket(Item):
    
    def __init__(self, data: tuple, salvageKit: str):
        super().__init__(data, salvageKit)
        self.detailed_type = data[4]
        self.upgrade_id = data[5]
        self.itemstat = data[6]
        self.value = self.get_value()
        
        #profit if item bought at buy_price
        self.buy_profit = self.value - self.buy_price
        #profit if item bought at sell_price (instabuy)
        self.sell_profit = self.value - self.buy_price
        
    def get_value(self, salvageKit="SF") -> float:
        if self.upgrade_id is not None and self.upgrade_id in self.item_prices["id"].values:
            upgrade_price = self.item_prices.loc[self.item_prices["id"] == self.upgrade_id, "sell_price"].iloc[0]
        else:
            upgrade_price = 0
        
        # amount of ectos * their price + price of the upgrrade
        # all multiplied by 0.85 to account for taxes incurred, then the cost of doing a salvage is subracted
        return (self.ecto_price * self.ectos.get(salvageKit) + upgrade_price) * 0.85 - self.salvage_cost.get(salvageKit)
        

class Backpack(Item):
    
    def __init__(self, data: tuple, salvageKit: str):
        super().__init__(data, salvageKit)
        self.detailed_type = data[4]
        self.upgrade_id = data[5]
        self.itemstat = data[6]
        self.value = self.get_value()
        
        #profit if item bought at buy_price
        self.buy_profit = self.value - self.buy_price
        #profit if item bought at sell_price (instabuy)
        self.sell_profit = self.value - self.buy_price
        
    def get_value(self, salvageKit="SF") -> float:
        if self.upgrade_id is not None and self.upgrade_id in self.item_prices["id"].values:
            upgrade_price = self.item_prices.loc[self.item_prices["id"] == self.upgrade_id, "sell_price"].iloc[0]
        else:
            upgrade_price = 0
        
        # amount of ectos * their price + price of the upgrrade
        # all multiplied by 0.85 to account for taxes incurred, then the cost of doing a salvage is subracted
        return (self.ecto_price * self.ectos.get(salvageKit) + upgrade_price) * 0.85 - self.salvage_cost.get(salvageKit)
    
        