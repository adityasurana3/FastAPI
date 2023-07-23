from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None

@app.get('/')
def root():
    return {'message': 'Hello World'}

@app.post('/post/')
def new_post(post: Post):
    print(post)
    return{'new_post':post}