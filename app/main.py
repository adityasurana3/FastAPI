from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
from typing import Optional


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    

my_posts = [{'title':'title 1','content':'Content of post1',"id":1},{'title':'title 2','content':'Content of post2',"id":2}]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
        
def find_post_index(id):
    for i,post in enumerate(my_posts):
        if post["id"] == id:
            return i


@app.get('/posts')
def get_posts():
    print("all")
    return {'data': my_posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def new_post(post: Post):
    post_dict = post.dict()
    my_posts.append(post_dict)
    return{'new_post':post_dict}

@app.get('/posts/{id}')
def get_posts(id: int):
    print("get1 post")
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")
    return {'post_detail':post}

@app.delete('/posts/{id}')
def delete_post(id: int):
    print("del")
    post_index = find_post_index(id)
    if post_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    
    my_posts.pop(post_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    print("updated")
    post_index = find_post_index(id)
    if post_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[post_index] = post_dict
    return{"data":post_dict}


