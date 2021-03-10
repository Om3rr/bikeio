import os
from dotenv import load_dotenv
import cloudinary
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("MYSQL_URL")
db = SQLAlchemy(app)
app.config['CORS_HEADERS'] = 'Content-Type'
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_NAME"),
    api_key=os.getenv("CLOUDINARY_KEY"),
    api_secret=os.getenv("CLOUDINARY_SECRET")
)
