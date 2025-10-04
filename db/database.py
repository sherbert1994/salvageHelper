# -*- coding: utf-8 -*-
"""
Created on Wed Oct  1 14:00:13 2025

@author: feysn
"""

from dotenv import load_dotenv
import os
import sqlite3
from sqlite3 import Error
import sys

load_dotenv(dotenv_path="config/.env")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.getenv("DB_NAME")

def create():    
    try:
        conn = get_connection()
        __create_itemstats(conn)
        __create_items(conn)
    finally:    
        conn.close()

def __create_itemstats(conn):
    query = """
        CREATE TABLE IF NOT EXISTS 'itemstats' (
            'itemstat_id' INTEGER NOT NULL,
            'name' TEXT NOT NULL,
            PRIMARY KEY('itemstat_id'));"""
    
    conn.execute(query)
    
def __create_items(conn):
    query = """
        CREATE TABLE IF NOT EXISTS 'items' (
            'item_id' INTEGER NOT NULL,
            'name' TEXT NOT NULL,
            'description' TEXT,
            'type' TEXT NOT NULL,
            'rarity' TEXT NOT NULL,
            'level' INTEGER NOT NULL,
            'detailed_type' TEXT,
            'weight' TEXT,
            'upgrade_id' INTEGER,
            'itemstat_id' INTEGER
            )
    """
    
    conn.execute(query)
       
def push_to_database(param_query: str, params_list: list[tuple]):
    try:
        conn = get_connection()
        cursor = conn.cursor()  
        
        cursor.executemany(param_query, params_list)
        conn.commit()
    except Error as e:
        print("Issue trying to connect to the sqlite database")
        print(e)
    finally:
        conn.close()
        
def get_known_itemstats_ids() -> list[int]:
    known_ids = []
    query = "SELECT itemstat_id FROM itemstats"
    try:
        conn = get_connection()
        cursor = conn.cursor()
        ids = cursor.execute(query)
        for i in ids:
            known_ids.append(i[0])
        
    except Error as e:
        print("Issue trying to connect to the sqlite database")
        print(e)
    finally:
        conn.close()
    
    return known_ids


def get_known_items_ids() -> list[int]:
    known_ids = []
    query = "SELECT item_id FROM items"
    try:
        conn = get_connection()
        cursor = conn.cursor()
        ids = cursor.execute(query)
        for i in ids:
            known_ids.append(i[0])
    finally:
        conn.close()
    
    return known_ids
     
def get_connection():
    try:
        return sqlite3.connect(DB_NAME)
    except Error as e:
        print("Issue trying to connect to the sqlite database")
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    create()

