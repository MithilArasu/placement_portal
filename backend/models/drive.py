from datetime import datetime
from extensions import db


class Drive(db.Model):
    __tablename__ = "drives"

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("companies.id"),
        nullable=False
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    salary = db.Column(
        db.Float
    )

    benefits = db.Column(
        db.Text
    )

    required_skills = db.Column(
        db.Text
    )

    eligibility_branch = db.Column(
        db.String(100)
    )

    minimum_cgpa = db.Column(
        db.Float
    )

    eligible_year = db.Column(
        db.Integer
    )

    deadline = db.Column(
        db.Date
    )

    status = db.Column(
        db.String(20),
        default="PENDING"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    applications = db.relationship(
        "Application",
        backref="drive",
        lazy=True
    )