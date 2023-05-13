from typing import Optional
from pydantic import BaseModel, Field

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