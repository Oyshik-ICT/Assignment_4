# import os

# class Config:
#     SECRET_KEY = 'your-secret-key'
#     ADMIN_REGISTRATION_CODE = "1818"
#     SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:p%40stgress@localhost:5433/dbname'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     JWT_SECRET_KEY = 'your-jwt-secret-key'


import os
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
    ADMIN_REGISTRATION_CODE = os.environ.get('ADMIN_REGISTRATION_CODE', '1818')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://postgres:p%40stgress@localhost:5433/postgres'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'default-jwt-secret-key')


    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
