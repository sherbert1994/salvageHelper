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
        __create_recipes(conn)
    except Error as e:
        print("Failed to create database. Is your .env file set up correctly?")
        print(e)
    finally:    
        conn.close()
        
def __create_itemstats(conn):
    query = """
        CREATE TABLE IF NOT EXISTS 'itemstats' (
            'itemstat_id' INTEGER NOT NULL,
            'name' TEXT NOT NULL,
            PRIMARY KEY('itemstat_id'));"""
    try:
        conn.execute(query)
    except Error as e:
        print("Failed to create itemstats table, exiting program...")
        print(e)
        sys.exit(1)
    
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
    
    try:
        conn.execute(query)
    except Error as e:
        print("Failed to create items table, exiting program...")
        print(e)
        sys.exit(1)

def __create_recipes(conn):
    query = """
        CREATE TABLE IF NOT EXISTS 'recipes' (
            'recipe_id' INTEGER NOT NULL,
            'output_id' INTEGER NOT NULL,
            'output_count' INTEGER NOT NULL,
            'item_1_id' INTEGER NOT NULL,
            'item_1_count' INTEGER NOT NULL,
            'item_2_id' INTEGER,
            'item_2_count' INTEGER,
            'item_3_id' INTEGER,
            'item_3_count' INTEGER,
            'item_4_id' INTEGER,
            'item_4_count' INTEGER,
            'item_5_id' INTEGER,
            'item_5_count' INTEGER,
            'artificer' BOOLEAN NOT NULL,
            'armorsmith' BOOLEAN NOT NULL,
            'chef' BOOLEAN NOT NULL,
            'homesteader' BOOLEAN NOT NULL,
            'huntsman' BOOLEAN NOT NULL,
            'jeweler' BOOLEAN NOT NULL,
            'leatherworker' BOOLEAN NOT NULL,
            'tailor' BOOLEAN NOT NULL,
            'weaponsmith' BOOLEAN NOT NULL,
            'scribe' BOOLEAN NOT NULL,
            'other' BOOLEAN NOT NULL
            )
    """
    
    try:
        conn.execute(query)
    except Error as e:
        print("Failed to create recipes table, exiting program...")
        print(e)
        sys.exit(1)
        
def push_to_database(param_query, params_list):
    try:
        conn = get_connection()
        cursor = conn.cursor()  
        cursor.executemany(param_query, params_list)
        conn.commit()
    except Error as e:
        print("Could not push to the database, skipping new rows")
        print(e)
    finally:
        conn.close()
        
def get_known_ids(table_name):
    if table_name == "itemstats":
        query = "SELECT itemstat_id FROM itemstats"
    elif table_name == "items":
        query = "SELECT item_id FROM items"
    elif table_name == "recipes":
        query = "SELECT recipe_id FROM recipes"
    known_ids= []
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        ids = cursor.execute(query)
        for i in ids:
            known_ids.append(i[0])
    except Error as e:
        print("Could not retrieve from the database, exiting program...")
        print(e)
        sys.exit(1)
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
