from fastapi import FastAPI, Body, Request
from fastapi.responses import HTMLResponse

app         = FastAPI()
app.title   = 'My FastAPI App'
app.version = "0.0.1"
# app.contact = {
#     "name": "Alex Maldonado",
#     "url": "https://github.com/alexmaldonado-cl/",
#     "email": "alex.maldonado@outlook.com"
# }

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

@app.get('/movies', tags=['movies'])
def get_movies():
    return movies

@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int):
	result = filter(lambda item : item['id'] == id, movies)
	result = list(result)
    
	return result

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str, year: int):
	result = filter(lambda item : item['category'] == category, movies)
	result = list(result)
    
	return result

@app.post('/movies', tags=['movies'])
def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
	movies.append({
		"id": id,
		"title": title,
		"overview": overview,
		"year": year,
		"rating": rating,
		"category": category
	})
	return movies

async def create_movie(request: Request):
	movie = await request.json()
	movies.append(movie)
	return movie
