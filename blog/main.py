from fastapi import FastAPI,Depends,status,Response,HTTPException
from . import schemas,models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session
tags_metadata = [
    {
        "name": "blogs",
        "description": "Blogs endpoints",
    }
    ]
app=FastAPI(title="Blog API",
    description="Blog API with CRUD functionality",
    version="0.0.1",openapi_tags=tags_metadata)

models.Base.metadata.create_all(engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()    

@app.post('/blog',status_code=status.HTTP_201_CREATED,tags=["blogs"])
def create(request:schemas.Blog,response:Response,db:Session=Depends(get_db)):
    new_blog=models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}',status_code=status.HTTP_200_OK,tags=["blogs"])
def destroy(id,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not available")
    blog.delete(synchronize_session=False) 
    db.commit()
    return {'details':"done"}

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED,tags=["blogs"])
def update(id,request:schemas.Blog,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not available")
    blog.update(request.dict(),synchronize_session=False)
    db.commit()
    return 'updated'



@app.get('/blog',tags=["blogs"])
def all(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}',status_code=200,tags=["blogs"])
def show(id,response:Response, db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()  
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not available")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail':f"Blog with the id {id} is not available"}
    return blog
       