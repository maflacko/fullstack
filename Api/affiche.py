from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
from pymongo import MongoClient
import bcrypt
import jwt
from datetime import datetime, timedelta
from functools import wraps
from dotenv import load_dotenv
import os

app = Flask(__name__)

#variables d'env
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

#config MongoDB
client = MongoClient("mongodb://mongo:27017/") 
db = client["artists"]  
collection = db["artists_collection"] 

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return jsonify({"error": "Token is missing or invalid"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(data, *args, **kwargs)
    return decorated

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/artists', methods=['GET'])
@token_required
def get_artists(user_data):
    page = int(request.args.get('page', 1)) 
    limit = int(request.args.get('limit', 10))  #artistes par page
    genre = request.args.get('genre', None) 
    skip = (page - 1) * limit 
    
    query = {}
    if genre: 
        query['genre'] = genre
    
    artists = collection.find(query).skip(skip).limit(limit)  
    total_artists = collection.count_documents(query) 
    
    return render_template(
        'index.html',
        artists=list(artists),
        user=user_data,
        page=page,
        limit=limit,
        total=total_artists,
        genre=genre
    )


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        #récupère les données du formulaire
        data = request.form
        username = data.get("username")
        password = data.get("password")

        if db["users"].find_one({"username": username}):
            return render_template('register.html', error="⚠️ L'utilisateur existe déjà. Veuillez en choisir un autre.")
        
        #hasher le mot de passe et creer l'user
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        db["users"].insert_one({"username": username, "password": hashed_password, "role": "user"})
        
        return render_template('login.html', message="Inscription réussie ! Veuillez vous connecter.")

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        data = request.form
        username = data.get("username")
        password = data.get("password")

        user = db["users"].find_one({"username": username})
        if not user:
            return render_template('login.html', error="⚠️ Nom d'utilisateur introuvable.")
        if not bcrypt.checkpw(password.encode('utf-8'), user["password"]):
            return render_template('login.html', error="⚠️ Mot de passe incorrect.")
        
        #token JWT
        token = jwt.encode(
            {"username": username, "exp": datetime.utcnow() + timedelta(hours=1)},
            SECRET_KEY,
            algorithm="HS256"
        )

        #ajoute le token dans un cookie
        response = make_response(redirect(url_for('get_artists')))
        response.set_cookie('token', token)
        return response
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
