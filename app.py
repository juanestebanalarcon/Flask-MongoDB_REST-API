from flask import Flask
from flask_pymongo import PyMongo

app = Flask("RESTAPI-STUDENTS-CRUD-MONGO_FLASK")
app.secret_key = "J100200300E00A00M"
app.config["MONGO_URI"] = "mongodb+srv://juanes:alarcon1@cluster0.azy840p.mongodb.net/students_flask"
mongo = PyMongo(app)
