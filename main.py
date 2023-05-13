from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie_router import movie_router
from routers.user_router import user_router

app = FastAPI()
app.title = 'My App of Movies'
app.version = '0.01'

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)

@app.get('/', tags=['Home'])
def root():
    #print(get_movie.__doc__)
    return HTMLResponse('<h1>My first APi with FastAPI</h1>')