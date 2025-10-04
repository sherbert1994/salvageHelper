# SalvageHelper

This python commandline program fetches data from the Guild Wars 2 API and a community-run Trading Post API for Guild Wars 2 to show you which items are currently profitable to buy and process

## Installation

Place the database in the same folder as main.py. If you do not have the database, it will be created and filled for you (slow, highly recommended to use partially prefilled database)

Go to the config folder, copy the contents of .env.example to a new .env and change {your_db_name} to the name of your db, if you are using the (partially) prefilled database. Make sure to include the file extension (default .db)

If you do not have the (partially) prefilled database, you can change {your_db_name} to anything you like (within reason, support for special characters and emojis very much untested)

Run the program from the commandline using "python main.py", with your current working directory being the one that has the main.py file.


## Features

Seeing profit for items using one of 2 salvage kits:
- Silver-Fed Salvage-o-matic
- Black Lion Salvage kit

Profits can be sorted by:
- Instantbuy of items
- Buy order of items

Sorted list can be:
- Viewed in terminal (top 50 most profitable items)
- Exported as csv (all items)