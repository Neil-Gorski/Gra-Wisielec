from unittest import result
from fastapi import Body, Request, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import json
from soupsieve import select
import sqlalchemy as db
import random
from app.model import CategoriesSchema, WordSchema




################################ DATABASE // SQLite  // SQLalchemy ############################################

engine = db.create_engine('sqlite:///Wisielec.db',connect_args={"check_same_thread": False})
metadata = db.MetaData()
connection = engine.connect()

categories = db.Table('Categories', metadata,
              db.Column('id', db.Integer(), primary_key=True, autoincrement=True),
              db.Column('name', db.String(60), nullable=False),
              db.Column('description', db.String(100), nullable=False)
              )

words = db.Table('Words', metadata,
              db.Column('id', db.Integer(), primary_key=True, autoincrement=True),
              db.Column('category_id', db.Integer(), nullable=False),
              db.Column('word', db.String(100), nullable=False),
              )

metadata.create_all(engine) 

################################ FastAPI #######################################################################

app = FastAPI()


@app.get("/categories", tags=["creat category"])
def get_categories():
    try:
        selectQuery = db.select([categories])
        conn = connection.execute(selectQuery)
        result = conn.fetchall()
    except Exception as err:
        print(err)
        return {"status": "faild"}
    else:
        return result
    

@app.post("/categories", tags=["post category"])
async def add_category(request: CategoriesSchema = Body(default=None)):
    # Parsujemy request i na jego podstawie wykonujemy edycje zasobu
    try:
        insertQuery = db.insert(categories).values(name=request.name, description=request.description)
        connection.execute(insertQuery)
        
    except Exception as err:
        print(err)
        return {"status": "faild"}
    else:
        return {"status": "done"}


@app.get("/categories/{id}", tags=["get category by ID"])
def get_categories_id(id: int):
    try:
        selectQuery = db.select([categories]).where(categories.columns.id == id)
        conn = connection.execute(selectQuery)
        result = jsonable_encoder(conn.fetchall())
        if result == []:
            return {"status": "faild", "Error": "No such categorie ID"}
    except Exception as err:
        print(err)
        return {"status": "faild", "Error": err}
    else:
        return result


@app.put("/categories/{id}", tags=["update category by ID"])
async def update_category(request: CategoriesSchema = Body(default=None)):
    try:
        selectQuery = db.select([categories]).where(categories.columns.id == request.id)
        conn = connection.execute(selectQuery)
        result = jsonable_encoder(conn.fetchall())
        if result == []:
            return {"status": "faild", "Error": "No such categorie ID"}
    except Exception as err:
        print(err)
        return {"status": "faild"}
    else:
        updateQuery = db.update(categories).where(categories.columns.id == request.id).values(name=request.name, description=request.description)
        connection.execute(updateQuery)
        return {"status": "updated"}


@app.delete("/categories/{id}", tags=["delete category by ID"])
async def delete_category(request: int):
    try:
        selectQuery = db.select([categories]).where(categories.columns.id == request)
        conn = connection.execute(selectQuery)
        result = jsonable_encoder(conn.fetchall())
        if result == []:
            return {"status": "faild", "Error": "No such categorie ID"}
    except Exception as err:
        print(err)
        return {"status": "faild"}
    else:
        deleteQuery = db.delete(categories).where(categories.columns.id == request)
        connection.execute(deleteQuery)
        return {"status": "deleted"}


@app.get("/words", tags=["get words"])
def get_words():
    try:
        selectQuery = db.select([words])
        conn = connection.execute(selectQuery)
        result = conn.fetchall()
    except Exception as err:
        print(err)
        return {"status": "faild"}
    else:
        return result
        

@app.get("/categories/{id}/word", tags=["get words by category ID"])
def get_words(category_id: int):
    try:
        selectQuery = db.select([words]).where(words.columns.category_id == category_id)
        conn = connection.execute(selectQuery)
        result = jsonable_encoder(conn.fetchall())
        if result == []:
            return {"status": "faild", "Error": "No such categorie ID"}
    except Exception as err:
        print(err)
        return {"status": "faild", "Error": err}
    else:
        return result


@app.post("/words", tags=["creat word"])
async def post_words(request: WordSchema = Body(default=None)):
    # Parsujemy request i na jego podstawie wykonujemy edycje zasobu
    try:
        print(request)
        selectQuery = db.select([words]).where(categories.columns.id == request.category_id)
        conn = connection.execute(selectQuery)
        result = jsonable_encoder(conn.fetchall())
        if result == []:
            return {"status": "faild", "Error": "No such categorie ID"}
    except Exception as err:
        print(err)
        return {"status": "faild"}
    else:
        insertQuery = db.insert(words).values(category_id=request.category_id, word=request.word)
        connection.execute(insertQuery)
        return {"status": "done"}


@app.put("/words", tags=["update word"])
async def update_word(request: WordSchema = Body(default=None)):
    try:
        selectQuery = db.select([words]).where(words.columns.id == request.id)
        conn = connection.execute(selectQuery)
        result = jsonable_encoder(conn.fetchall())
        if result == []:
            return {"status": "faild", "Error": "No such word ID"}
    except Exception as err:
        print(err)
        return {"status": "faild"}
    else:
        updateQuery = db.update(words).where(words.columns.id == request.id).values(category_id=request.category_id, word=request.word)
        connection.execute(updateQuery)
        return {"status": "updated"}


@app.delete("/words/{id}", tags=["delete word by ID"])
async def delete_word(request: int):
    try:
        selectQuery = db.select([words]).where(words.columns.id == request)
        conn = connection.execute(selectQuery)
        result = jsonable_encoder(conn.fetchall())
        if result == []:
            return {"status": "faild", "Error": "No such word ID"}
    except Exception as err:
        print(err)
        return {"status": "faild"}
    else:
        deleteQuery = db.delete(words).where(words.columns.id == request)
        connection.execute(deleteQuery)
        return {"status": "deleted"}

@app.get("/words/random", tags=["get random word"])
def get_word():
    try:
        selectQuery = db.select([words]).order_by(db.func.random()).limit(1)
        conn = connection.execute(selectQuery)
        result = jsonable_encoder(conn.fetchall())
        if result == []:
            return {"status": "faild", "Error": "No such word ID"}
    except Exception as err:
        print(err)
        return {"status": "faild", "Error": err}
    else:
        return result












