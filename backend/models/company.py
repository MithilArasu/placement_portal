from extensions import db


class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    company_name = db.Column(
        db.String(150),
        nullable=False
    )

    industry = db.Column(db.String(100))

    location = db.Column(db.String(100))

    website = db.Column(db.String(255))

    hr_contact = db.Column(db.String(100))

    approval_status = db.Column(
        db.String(20),
        default="PENDING"
    )

    is_blacklisted = db.Column(
        db.Boolean,
        default=False
    )

    drives = db.relationship(
        "Drive",
        backref="company",
        lazy=True
    )

    placements = db.relationship(
        "Placement",
        backref="company",
        lazy=True
    )