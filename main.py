# -*- coding: utf-8 -*-
"""
Created on Wed Oct  1 19:43:31 2025

@author: feysn
"""

from db import database, api_connect


if __name__ == "__main__":
    database.create()
    api_connect.update_itemstats()
    api_connect.update_items()