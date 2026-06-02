import os

class Config:
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'secret')
    DB_NAME = os.environ.get('DB_NAME', 'seminar_db')
    DB_PORT = int(os.environ.get('DB_PORT', 3306))