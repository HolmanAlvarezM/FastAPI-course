from fastapi import FastAPI, HTTPException, Request, Path, Query, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from starlette.requests import Request
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie

app = FastAPI()
app.title = 'My App of Movies'
app.version = '0.01'

email = "admin@gmail.com"
password = "admin"

Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != email:
            raise HTTPException(status_code=403, detail="Credentials invalid")

class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id: Optional[int]
    title: str = Field(min_length=5, max_length=30)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2023)
    rating: int = Field(gt=0, le=10)
    category: str = Field(min_length=5, max_length=10)
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "No named",
                "overview": "Overview of movie",
                "year": 1900,
                "rating": 1.0,
                "category": "No category"
            }
        }

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Drama'    
    }
]

@app.get('/', tags=['Home'])
def root():
    #print(get_movie.__doc__)
    return HTMLResponse('<h1>My first APi with FastAPI</h1>')

@app.post('/login', tags=['Auth'], status_code=200)
def login(user: User):
    if user.email == email and user.password == password:
        token:str = create_token(user.dict())
    return JSONResponse(content=token, status_code=200)

@app.get('/movies', tags=['Movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    """
        Consult all movies in database
        Parameters: None
        Returns: Json with all the movies in database
    """
    return JSONResponse(status_code=200, content=movies)

@app.get('/movies/{id}', tags=['Movies'], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=10000)) -> Movie:
    """
        Search movie by id
        Parameters: id (int): identificator of movie
        Returns: Json with data of the selected movie or empty list if don't exist id
    """
    data = [movie for movie in movies if movie['id'] == id]
    return JSONResponse(status_code=200, content=data)

@app.get('/movies/', tags=['Movies'], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=20)) -> List[Movie]:
    """
        Consult all movies by category, function of type Query
        Parameters: category (str): category of search
        Returns: Json with movies of category or empty list if don't exist id
    """
    data = [movie for movie in movies if movie['category'] == category]
    return JSONResponse(status_code=200, content=data)

@app.post('/movies', tags=['Movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201, content={"message":"Movie was register"})

""" @app.post('/movies', tags=['Movies'])
async def create_movie(request: Request):
    movie = await request.json()
    movies.append(movie)
    return movies
"""

""" @app.put('/movies/{id}', tags=['Movies'])
async def update_movie(id: int, request: Request):
    movie = await request.json()
    for index, item in enumerate(movies):
        if item["id"] == id:
            movies[index].update(movie)
            return movies[index]
        
    raise HTTPException(status_code=404, detail='Movie not found') 
"""

@app.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    for index, item in enumerate(movies):
        if item["id"] == id:
            movies[index].update(movie)
            movies[index]["id"] = id
            return JSONResponse(status_code=200, content={"message":"Movie was modify"})

@app.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
async def delete_movie(id: int) -> dict:
    for index, item in enumerate(movies):
        if item["id"] == id:
            del movies[index]
            return JSONResponse(status_code=200, content={"message":"Movie was delete"})
    raise HTTPException(status_code=404, detail="Movie not found")