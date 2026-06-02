from flask import Flask
from app.routes import bp

def create_app():
    app = Flask(__name__)
    
    # API 블루프린트 등록
    app.register_blueprint(bp)
    
    return app