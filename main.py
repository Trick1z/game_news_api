from typing import Union
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, File, Response, status, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import pandas as pd
import mysql.connector
from mysql.connector import Error
from pydantic import BaseModel
from datetime import datetime
from dotenv import load_dotenv
import os
import base64
from dateutil import parser
import pytz
import io
import csv
from openpyxl import load_workbook
import hashlib
from bs4 import BeautifulSoup
import time
load_dotenv()


# get DB
def get_DB():
    # deploy docker
    # connector = mysql.connector.connect(
    #     host='host.docker.internal',
    #     user='root',
    #     database='mydb'
    # )

    # localhost
    connector = mysql.connector.connect(
        host='localhost',
        user='root',
        database='game_news'
    )

    return connector


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "*"],  # List allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class services ():
    def getTime():

        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return current_datetime


class query():
    def get(order: str):
        cnx = get_DB()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(order)
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()

        return rows

    def post(order: str):
        cnx = get_DB()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(order)

        # rows = cursor.fetchall()
        # cursor.close()
        # cnx.close()
#
        # cnx.commit()
        # cursor.close()
        # cnx.close()
#
        cnx.commit()
        id = cursor.lastrowid
        cursor.close()
        cnx.close()
        return {"message": 200, "id": id}

    def put(order: String):
        cnx = get_DB()
        cursor = cnx.cursor()
        cursor.execute(order)
        cnx.commit()
        cursor.close()
        cnx.close()

        return {"status": 200, "msg": 'update has change'}


class mainData (BaseModel):
    MAIN_TITLE: str
    MAIN_DESC: str
    IMG: str


@app.post('/post.main')
def post_main(data: mainData):

    try:
        res = query.post(
            f"INSERT INTO main (MAIN_TITLE,MAIN_DESC) VALUES ('{data.MAIN_TITLE}','{data.MAIN_DESC}')")
        main_id = res["id"]

        res_img = query.post(
            f"INSERT INTO img (IMG_IMG , MAIN_ID  ) VALUES ('{data.IMG}' , {main_id} )")
        return {'main': res,
                'img': res_img}
    except Exception as e:
        return e


# post sub data
class subData (BaseModel):
    MAIN_ID: int
    SUB_TITLE: str
    SUB_DESC: str
    YOUTUBE: str
    STEAM: str
    SUB_DETAIL: str


@app.post('/post.sub')
def post_sub(data: subData):
    try:
        res = query.post(
            f"INSERT INTO sub (MAIN_ID , SUB_TITLE , SUB_DESC  , YOUTUBE , STEAM ,SUB_DETAIL) VALUES ({data.MAIN_ID} , '{data.SUB_TITLE}' , '{data.SUB_DESC}' , '{data.YOUTUBE}' ,'{data.STEAM}' ,'{data.SUB_DETAIL}')")
        return res
    except Exception as e:
        return e


# get main data

@app.get('/get.main')
def get_main():
    try:
        res = query.get(
            f"SELECT MAIN_ID , MAIN_TITLE , MAIN_DESC FROM main WHERE DEL_FRAG = 'N'")

        return res
    except Exception as e:
        raise e

# get edit


@app.get('/get.edit/ref_main={id}')
def get_edit_data(id: int):
    try:
        res = query.get(f"""SELECT
                            m.*,
                            i.IMG_IMG,
                            s.SUB_TITLE,
                            s.SUB_DETAIL,
                            s.SUB_DESC,
                            s.YOUTUBE ,
                            s.STEAM
                            FROM main m
                            INNER JOIN img i ON m.MAIN_ID = i.MAIN_ID
                            INNER JOIN sub s ON m.MAIN_ID = s.MAIN_ID
                            WHERE m.MAIN_ID = {id};""")
        return res
    except Exception as e:
        return e
    
    
# put edit 
class editData(BaseModel):
    MAIN_ID : int 
    MAIN_TITLE: str
    MAIN_DESC :str
    IMG_IMG : str
    SUB_TITLE :str
    SUB_DESC :str
    SUB_DETAIL :str
    YOUTUBE : str
    STEAM : str
    
app.put('/put.edit')
def put_edit_data(data : editData):
    try:
        res = 
        return
    except Exception as e:
        return e