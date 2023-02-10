from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService

movie_router = APIRouter()

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


@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
	db     = Session()
	result = MovieService(db).get_movies()
	return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['movies'])
def get_movie(id: int = Path(ge=1, le=2000)):
	db = Session()
	result = MovieService(db).get_movie(id)
	if not result:
		return JSONResponse(status_code=404, content={'message': 'Movie not found'})

	return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
	db     = Session()
	result = MovieService(db).get_movies_by_category(category)
	return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
	db = Session()
	new_movie = MovieModel(**movie.dict())
	db.add(new_movie)
	db.commit()
	# movies.append(movie)
	return JSONResponse(status_code=201, content={"message": "Movie registered successfully"})

# async def create_movie(request: Request):
# 	movie = await request.json()
# 	movies.append(movie)
# 	return movie


@movie_router.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, movie: Movie):

	db     = Session()
	result = db.query(MovieModel).filter(MovieModel.id == id).first()
	if not result:
		return JSONResponse(status_code=404, content={'message': 'Movie not found'})
	
	result.title    = movie.title
	result.overview = movie.overview
	result.year     = movie.year
	result.rating   = movie.rating
	result.category = movie.category

	db.commit()

	return JSONResponse(status_code=200, content={"message": "Edited movie successfully"})

@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict)
def delete_movie(id: int) -> dict:

	db     = Session()
	result = db.query(MovieModel).filter(MovieModel.id == id).first()
	if not result:
		return JSONResponse(status_code=404, content={'message': 'Movie not found'})

	db.delete(result)
	db.commit()

	return JSONResponse(status_code=200, content={"message": "Deleted movie successfully"})