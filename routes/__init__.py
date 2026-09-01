from .xmlibris_routes import xmlibris_bp
from .auth_routes import auth_bp
from .users_routes import users_bp


blueprints = [
    (xmlibris_bp, "/xmlibris"),
    (auth_bp, "/auth"),
    (users_bp, "/users"),
]
