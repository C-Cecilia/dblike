import sqlalchemy as sqla
from sqlalchemy import create_engine
import traceback
import glob
import os 
from pprint import pprint
import simplejson as json
import requests
import time
from IPython.display import display

URL= "dbbike.c2pot9zcoud2.eu-west-1.rds.amazonaws.com"
PORT="3306"
DB="dbbike"
USER="admin"
PASSWORD="DBbike30830" 

engine = create_engine(("mysql+mysqldb://{}:{}@{}:{}/{}").format(USER,PASSWORD,URL,PORT,DB),echo=True)

# sql = """ CREATE DATABASE IF NOT EXISTS dbike; """

# engine.execuet(sql)

res=engine.execute("Select * from station")
print(res.fetchall())




