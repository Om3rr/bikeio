from app import app
from routes.bikeapi import bikeapi_bp

app.register_blueprint(bikeapi_bp, url_prefix='/bikeapi')

if __name__ == "__main__":
    app.run()
