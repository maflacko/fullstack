from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

#configuration MongoDB
client = MongoClient("mongodb://mongo:27017/") 
db = client["artists"]  
collection = db["artists_collection"] 

@app.route('/')
def index():
    #Récupère tous les documents de la collection
    artists = collection.find({})
    #Renvoie le template HTML avec les données des artistes
    return render_template('index.html', artists=list(artists))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
