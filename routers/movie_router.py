from fastapi import APIRouter, HTTPException, Path, Query, Depends
from fastapi.encoders import jsonable_encoder
from config.database import Session
from typing import List
from fastapi.responses import JSONResponse
from middlewares.jwt_bearer import JWTBearer
from services.movie_service import MovieService
from schemas.movie_schema import Movie

movie_router = APIRouter()

@movie_router.get('/movies', tags=['Movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    """
        Consult all movies in database
        Parameters: None
        Returns: Json with all the movies in database
    """
    db = Session()
    result = MovieService(db).get_movies()    
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['Movies'], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=10000)) -> Movie:
    """
        Search movie by id
        Parameters: id (int): identificator of movie
        Returns: Json with data of the selected movie or empty list if don't exist id
    """
    db = Session()
    result = MovieService(db).get_movie(id)
    
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
    result = MovieService(db).get_movies_by_category(category)
    
    if not result:
        return JSONResponse(status_code=404, content={"message":"Not result data"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.post('/movies', tags=['Movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201, content={"message":"Movie was register"})

@movie_router.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    
    if not result:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    
    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code=200, content={"message":"Movie was modify"})

@movie_router.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
async def delete_movie(id: int) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Movie not found")
               
    MovieService(db).delete_movie(id)
    raise HTTPException(status_code=200, detail="Movie was delete")    