import os

class Config:
    # SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret')
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:123456@localhost/ponto')
    SECRET_KEY = os.getenv('SECRET_KEY')
    print(SECRET_KEY)
    print(os.getenv('DATABASE_URL'))
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False