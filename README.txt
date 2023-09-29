export FLASK_APP=RecipeBook
flask run

export to env variables and reading from it: 
os.environ.get('SECRET_KEY')

another way : 
app.config.from_prefixed_env()
FLASK_SECRET_KEY -> SECRET_KEY (drops the FLASK prefix)

create the database : 
from ReciepeBook import db, create_app
db.create_all(app=create_app())

session management :
flask-login : https://youtu.be/J76B74PZQ_Y?list=PL9UJyHy1Xn3oY1qhpOyCkulufX66eUJA5
