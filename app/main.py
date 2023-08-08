from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)



while True:
    try:
        conn = psycopg2.connect(database='fastapi', user='postgres', password='admin', host='localhost',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected")
        break
    except Exception as error:
        print("Connection to data base failed")
        print("Error: ", error)

my_posts = [{'title': 'title 1', 'content': 'Content of post1', "id": 1},
            {'title': 'title 2', 'content': 'Content of post2', "id": 2}]


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post


def find_post_index(id):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            return i


