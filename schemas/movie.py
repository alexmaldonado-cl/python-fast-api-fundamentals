from pydantic import BaseModel, Field
from typing import Optional, List

class Movie(BaseModel):
	id: Optional[int] = None
	title: str = Field(min_length=5, max_length=25)
	overview: str = Field(min_length=15, max_length=150)
	year: int = Field(le=2022)
	rating: float
	category: str

	class Config:
		schema_extra = {
			"example": {
				"id": 1,
				"title": "Mi pelicula",
				"overview": "Descripción de la pelicula",
				"year": 2022,
				"rating": 9.7,
				"category": "Action"
			}
		}