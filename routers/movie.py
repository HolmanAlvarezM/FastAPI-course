from fastapi import APIRouter, HTTPException, Path, Query, Depends
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from config.database import Session
from typing import Optional, List
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from middlewares.jwt_bearer import JWTBearer

movie_router = APIRouter()

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

@movie_router.get('/movies', tags=['Movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    """
        Consult all movies in database
        Parameters: None
        Returns: Json with all the movies in database
    """
    db = Session()
    result = db.query(MovieModel).all()    
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['Movies'], response_model=Movie, status_code=200)
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

@movie_router.get('/movies/', tags=['Movies'], response_model=List[Movie], status_code=200)
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

@movie_router.post('/movies', tags=['Movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={"message":"Movie was register"})

@movie_router.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
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

@movie_router.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
async def delete_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Movie not found")
               
    db.delete(result)
    db.commit()
    raise HTTPException(status_code=200, detail="Movie was delete")    