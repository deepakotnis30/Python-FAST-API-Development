
from fastapi import Body, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy import func
from app import oauth2
from .. import models, schemas
from .. database import engine, get_db
from typing import Optional, List

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO POSTS(title, content, published) VALUES (%s,%s,%s) RETURNING * """,
    #              (post.title, post.content, post.published))
    #new_post =cursor.fetchone()
    #conn.commit()    
    new_post = models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    

#update post

@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("UPDATE posts SET title=%s, content=%s, published=%s where id=%s RETURNING *", 
    #               (post.title, post.content, post.published, id))
    #updated_post =cursor.fetchone()
    #conn.commit()    
    #index = find_index_post(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()  
  

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    if updated_post.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(updated_post)
    return updated_post


#@router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0,search: Optional[str] = ""):

    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() 
    
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    #print(posts)
    return posts

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id:int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    #post = cursor.fetchone()
    #print(post)
    #post = find_post(id)
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    #print(post)
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")     
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("DELETE FROM posts WHERE id = %s returning *", (id,))
    #delete_post =cursor.fetchone()
    #conn.commit()    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)