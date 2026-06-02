from extensions import db


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    register_number = db.Column(
        db.String(50),
        unique=True
    )

    branch = db.Column(
        db.String(100)
    )

    cgpa = db.Column(
        db.Float
    )

    year = db.Column(
        db.Integer
    )

    skills = db.Column(
        db.Text
    )

    resume_path = db.Column(
        db.String(255)
    )

    experience = db.Column(
        db.Text
    )

    phone = db.Column(
        db.String(20)
    )

    is_blacklisted = db.Column(
        db.Boolean,
        default=False
    )

    applications = db.relationship(
        "Application",
        backref="student",
        lazy=True
    )

    placements = db.relationship(
        "Placement",
        backref="student",
        lazy=True
    )