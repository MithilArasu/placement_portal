from app import app
from extensions import db
from models import User


def create_admin():

    with app.app_context():

        admin = User.query.filter_by(
            email="admin@placementportal.com"
        ).first()

        if admin:
            print("Admin already exists")
            return

        admin = User(
            email="admin@placementportal.com",
            role="ADMIN"
        )

        admin.set_password("admin123")

        db.session.add(admin)
        db.session.commit()

        print("Admin created successfully")


if __name__ == "__main__":
    create_admin()