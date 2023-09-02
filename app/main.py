from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(auth.router)


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


