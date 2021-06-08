import sqlite3
from sqlite3 import Error
import os
import pandas as pd
import time
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt


def create_connection(db_file): # create a database
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()


def create_table(_db):
    db = _db
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS data (name text, data text)')

def add_rows():
    pass

def add_data():
    pass

# create_connection("CondExpData.db")
# create_table("CondExpData.db")

def parseTextToCSV(dir, destinationFileName):

    dirfiles = [] # create empty array for the file names
    # dirwalk the dir and get all files that meet the criteria
    for root, dirs, files in os.walk(dir):
        dirs.sort()
        for filename in files:
            # print(filename)
            if filename.endswith(".txt"):
                dirfiles.append((os.path.join(root, filename)))
            if filename.endswith(".csv"):
                dirfiles.append((os.path.join(root, filename)))
    dirfiles = sorted(dirfiles) # sort the dirfiles

    set_csv = dir +"/"+ destinationFileName + ".csv" #set up the CSV file

    # write headers and first file
    print("Start.")
    file = dirfiles[1]
    parsed_file = pd.read_csv(file, sep='\t', header=3, skip_blank_lines=True, skiprows=range(4,8))
    parsed_file.to_csv(set_csv, sep=",", header=True)

    # set up progress bar
    pbar_total = len(dirfiles)
    pbar_increment = 1
    pbar = tqdm(total=pbar_total)

    # write all other files
    with open(set_csv, 'a') as f:

        for i in dirfiles[1:]:
            try:
                parsed_file = pd.read_csv(i, sep='\t', skiprows=range(0, 8))
                parsed_file.to_csv(f, header=False)
            except:
                parsed_file = pd.read_csv(i, sep='\t', skiprows=range(0, 15))
                parsed_file.to_csv(f, header=False)
            pbar.update(pbar_increment)  # update progress bar

    time.sleep(1)
    pbar.close()
    f.close()
    print("Complete!")




