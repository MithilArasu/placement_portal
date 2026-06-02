from flask import Flask

from config import Config
from extensions import db, jwt, migrate
from routes.admin import admin_bp
from routes.company import company_bp
from routes.student import student_bp
from models import (
    User,
    Student,
    Company,
    Drive,
    Application,
    Placement
)

from routes.auth import auth_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(
    auth_bp,
    url_prefix="/auth"
    )

    app.register_blueprint(
        admin_bp,
        url_prefix="/admin"
    )

    app.register_blueprint(
        company_bp,
        url_prefix="/company"
    )
    app.register_blueprint(
        student_bp,
        url_prefix="/student"
    )

    @app.route("/")
    def home():
        return {
            "message": "Placement Portal Backend Running"
        }

    @app.route("/test-db")
    def test_db():
        return {
            "users_table": User.__tablename__,
            "students_table": Student.__tablename__,
            "companies_table": Company.__tablename__,
            "drives_table": Drive.__tablename__,
            "applications_table": Application.__tablename__,
            "placements_table": Placement.__tablename__
        }

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)