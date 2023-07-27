from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, SessionLocal 
from sqlalchemy.orm import Session
from fastapi import Depends

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    

while True:
    try:
        conn = psycopg2.connect(database='fastapi',user='postgres',password='admin',host='localhost',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected")
        break
    except Exception as error:
        print("Connection to data base failed")
        print("Error: ",error)

my_posts = [{'title':'title 1','content':'Content of post1',"id":1},{'title':'title 2','content':'Content of post2',"id":2}]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
        
def find_post_index(id):
    for i,post in enumerate(my_posts):
        if post["id"] == id:
            return i


@app.get('/sql')
def get_sql(db: Session = Depends(get_db)):
    return{'db':'success'}

@app.get('/posts')
def get_posts():
    cursor.execute(''' SELECT * from posts ''')
    post = cursor.fetchall()
    return {'data': post}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def new_post(post: Post):
    cursor.execute(""" INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    post = cursor.fetchone()
    conn.commit()
    return{'new_post':post}

@app.get('/posts/{id}')
def get_posts(id: int):
    cursor.execute(""" SELECT * from posts where id=%s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")
    return {'post_detail':post}

@app.delete('/posts/{id}')
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts where id=%s RETURNING *""",str(id))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title=%s, content = %s, published=%s WHERE id=%s RETURNING *""",(post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    return{"data":updated_post}


