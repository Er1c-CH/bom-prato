from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:3742@localhost:5432/bomprato'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = '（っ＾▿＾）'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)