from fastapi import FastAPI, HTTPException, Path, Query, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer

app = FastAPI()
app.title = 'My App of Movies'
app.version = '0.01'
app.add_middleware(ErrorHandler)

Base.metadata.create_all(bind=engine)

class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id: Optional[int]
    title: str = Field(min_length=5, max_length=30)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2023)
    rating: int = Field(gt=0, le=10)
    category: str = Field(min_length=5, max_length=15)
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "No named movie",
                "overview": "Overview of movie",
                "year": 1900,
                "rating": 1.0,
                "category": "No category"
            }
        }

@app.get('/', tags=['Home'])
def root():
    #print(get_movie.__doc__)
    return HTMLResponse('<h1>My first APi with FastAPI</h1>')

@app.post('/login', tags=['Auth'], status_code=200)
def login(user: User):
    if user.email == JWTBearer.email and user.password == JWTBearer.password:
        token:str = create_token(user.dict())
    return JSONResponse(content=token, status_code=200)

@app.get('/movies', tags=['Movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    """
        Consult all movies in database
        Parameters: None
        Returns: Json with all the movies in database
    """
    db = Session()
    result = db.query(MovieModel).all()    
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get('/movies/{id}', tags=['Movies'], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=10000)) -> Movie:
    """
        Search movie by id
        Parameters: id (int): identificator of movie
        Returns: Json with data of the selected movie or empty list if don't exist id
    """
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    
    if not result:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get('/movies/', tags=['Movies'], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=20)) -> List[Movie]:
    """
        Consult all movies by category, function of type Query
        Parameters: category (str): category of search
        Returns: Json with movies of category or empty list if don't exist id
    """
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    
    if not result:
        return JSONResponse(status_code=404, content={"message":"Not result data"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.post('/movies', tags=['Movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={"message":"Movie was register"})

@app.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    
    if not result:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    return JSONResponse(status_code=200, content={"message":"Movie was modify"})

@app.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
async def delete_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Movie not found")
               
    db.delete(result)
    db.commit()
    raise HTTPException(status_code=200, detail="Movie was delete")    