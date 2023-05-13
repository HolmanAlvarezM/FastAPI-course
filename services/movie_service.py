from models.movie_model import Movie as MovieModel
from schemas.movie_schema import Movie

class MovieService():
    
    def __init__(self, db) -> None:
        self.db = db
        
    def get_movies(self):
        movies = self.db.query(MovieModel).all()
        return movies
    
    def get_movie(self, id):
        movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return movie
    
    def get_movies_by_category(self, category):
        movies = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return movies
    
    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()
        return
    
    def update_movie(self, id, data: Movie):
        movie = self.get_movie(id)
        movie.title = data.title
        movie.overview = data.overview
        movie.year = data.year
        movie.rating = data.rating
        movie.category = data.category
        self.db.commit()
        return
    
    def delete_movie(self, id):
        movie = self.get_movie(id)
        self.db.delete(movie)
        self.db.commit()
        return