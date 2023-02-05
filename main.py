from fastapi import FastAPI, Body, Request, HTTPException, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app         = FastAPI()
app.title   = 'My FastAPI App'
app.version = "0.0.1"
# app.contact = {
#     "name": "Alex Maldonado",
#     "url": "https://github.com/alexmaldonado-cl/",
#     "email": "alex.maldonado@outlook.com"
# }

class Movie(BaseModel):
	id: Optional[int] = None
	title: str = Field(min_length=5, max_length=15)
	overview: str = Field(min_length=15, max_length=50)
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



movies = [
    {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Action"
	},
    {
		"id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Drama"
	}
]

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')

@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int = Path(ge=1, le=2000)):
	result = filter(lambda item : item['id'] == id, movies)
	result = list(result)
    
	return JSONResponse(content=result)

@app.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
	result = filter(lambda item : item['category'] == category, movies)
	result = list(result)
    
	return JSONResponse(status_code=200, content=result)

@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
	movies.append(movie)
	return JSONResponse(status_code=201, content={"message": "Pelicula registrada"})

# async def create_movie(request: Request):
# 	movie = await request.json()
# 	movies.append(movie)
# 	return movie


@app.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, movie: Movie):
	result = filter(lambda item : item['id'] == id, movies)
	result = list(result)
	# print(result[0])
	if(result[0]):
		result[0]["title"]    = movie.title
		result[0]["overview"] = movie.overview
		result[0]["year"]     = movie.year
		result[0]["rating"]   = movie.rating
		result[0]["category"] = movie.category
	return JSONResponse(content={"message": "Se ha modificado la Pelicula"})

@app.delete('/movies/{id}', tags=['movies'], response_model=dict)
def delete_movie(id: int) -> dict:
	for index, item in enumerate(movies):
		if item["id"] == id:
			del movies[index]
			return JSONResponse(content={"message": "Pelicula eliminada"})
	
	raise HTTPException(status_code=404, detail="Movie not found")