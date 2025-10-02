# -*- coding: utf-8 -*-
"""
Created on Wed Oct  1 17:28:37 2025

@author: feysn
"""

import pandas as pd


# returns all items with their prices. Items that have no price (NaN or 0) are omitted
def get_item_prices() -> pd.DataFrame:
    url = "https://api.datawars2.ie/gw2/v1/items/csv?fields=id,buy_price,sell_price"
    
    item_prices = pd.read_csv(url)
    #Drop the rows where both buy_price and sell_price are NaN
    item_prices = item_prices[item_prices["buy_price"].notna() | item_prices["sell_price"].notna()]
    item_prices = item_prices[(item_prices["buy_price"] != 0) & (item_prices["sell_price"] != 0)]
    #NaN values are gone, we can now set types properly as buy_price and sell_price are returned as floats, but for our case we will only use them as int
    item_prices = item_prices.astype({"id": "int64", "buy_price": "int64", "sell_price": "int64"}) 
    
    return item_prices

item_prices = get_item_prices()
