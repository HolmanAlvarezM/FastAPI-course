from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()
app.title = 'My App of Movies'
app.version = '0.01'

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

@app.get('/movies', tags=['Movies'])
def get_movies():
    """
        Consult all movies in database
        Parameters: None
        Returns: Json with all the movies in database
    """
    return movies

@app.get('/movies/{id}', tags=['Movies'])
def get_movie(id: int):
    """
        Search movie by id
        Parameters: id (int): identificator of movie
        Returns: Json with data of the selected movie or empty list if don't exist id
    """
    return [movie for movie in movies if movie['id'] == id]

@app.get('/movies/', tags=['Movies'])
def get_movies_by_category(category: str):
    """
        Consult all movies by category, function of type Query
        Parameters: category (str): category of search
        Returns: Json with movies of category or empty list if don't exist id
    """
    return [movie for movie in movies if movie['category'] == category]

@app.post('/movies', tags=['Movies'])
def create_movie(movie: Movie):
    movies.append(movie)
    return movies

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

@app.put('/movies/{id}', tags=['Movies'])
def update_movie(id: int, movie: Movie):
    for index, item in enumerate(movies):
        if item["id"] == id:
            movies[index].update(movie)
            movies[index]["id"] = id
            return movies[index]

@app.delete('/movies/{id}', tags=['Movies'])
async def delete_movie(id: int):
    for index, item in enumerate(movies):
        if item["id"] == id:
            del movies[index]
            return {'status': 'deleted movie'}

    raise HTTPException(status_code=404, detail="Movie not found")