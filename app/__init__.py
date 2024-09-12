from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Registra le blueprint delle route
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
