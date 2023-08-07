from ..utils import hash_password
from fastapi import status, HTTPException, Response, Depends
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import APIRouter
from typing import List

router = APIRouter()

@router.get('/posts', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(''' SELECT * from posts ''')
    # post = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def new_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/posts/{id}')
def get_posts(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * from posts where id=%s """, (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")
    return post


@router.delete('/posts/{id}')
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


@router.put('/posts/{id}')
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title=%s, content = %s, published=%s WHERE id=%s RETURNING *""",(post.title,
    # post.content, post.published, str(id))) updated_post = cursor.fetchone() conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}
