from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas
from .database import engine, SessionLocal 
from sqlalchemy.orm import Session
from fastapi import Depends
from .utils import hash_password

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


@app.get('/posts', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(''' SELECT * from posts ''')
    # post = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def new_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get('/posts/{id}')
def get_posts(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * from posts where id=%s """, (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")
    return post

@app.delete('/posts/{id}')
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts where id=%s RETURNING *""",str(id))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    delete_post = db.query(models.Post).filter(models.Post.id == id)
    if delete_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    delete_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put('/posts/{id}')
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title=%s, content = %s, published=%s WHERE id=%s RETURNING *""",(post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return{"data":post_query.first()}


@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user