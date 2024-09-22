import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    #SECRET_KEY = os.environ.get("SECRET_KEY") or "hard_to_guess_string"
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:students@localhost/SDK_DB"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
