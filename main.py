from fastapi import FastAPI
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
		"category": "Acción"
	},
    {
		"id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
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