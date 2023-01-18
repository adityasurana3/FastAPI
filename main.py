from fastapi import FastAPI, HTTPException, status, Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

class Post(BaseModel):
    title:str
    content:str
    published:bool
    rating:Optional[int] = None

app=FastAPI()

my_posts = [{'title':'Hello There','content':'Hello FastApi','id':1},{'title':'Computer Languages','content':'Python, C/C++','id':2}]

def fetch_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_page_index(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get('')
def root():
    return {'message':'Hello World'}

@app.get('/posts')
def get_posts():
    return {'message':my_posts}

@app.get('/posts/{id}')
def get_post(id:int):
    print(id)
    post=fetch_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Not Found')
    return {'detail':f'The id you entered is {post}'}


@app.post('/posts',status_code=status.HTTP_201_CREATED)
def createpost(post:Post):
    # To convert the data in python Dictionary
    post_dict=post.dict()
    post_dict['id'] = randrange(1,1000000)
    my_posts.append(post)
    return {'newpost':post_dict}
    
@app.delete('/delete/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index=find_page_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Index does not exist')
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id:int,post:Post):
    index=find_page_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Index does not exist')
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data':post_dict}