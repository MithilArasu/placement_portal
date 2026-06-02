from datetime import datetime
from extensions import db


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    drive_id = db.Column(
        db.Integer,
        db.ForeignKey("drives.id"),
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="APPLIED"
    )

    feedback = db.Column(
        db.Text
    )

    interview_date = db.Column(
        db.DateTime
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    __table_args__ = (
        db.UniqueConstraint(
            "student_id",
            "drive_id",
            name="unique_application"
        ),
    )