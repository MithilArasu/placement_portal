from flask import Blueprint

from flask_jwt_extended import get_jwt_identity

from utils.decorators import student_required

from extensions import db

from models import (
    Student,
    Drive,
    Application,
    Placement
)

student_bp = Blueprint(
    "student",
    __name__
)


@student_bp.route("/dashboard")
@student_required
def dashboard():

    return {
        "message": "Welcome Student"
    }


@student_bp.route("/drives")
@student_required
def get_drives():

    drives = Drive.query.filter_by(
        status="APPROVED"
    ).all()

    data = []

    for drive in drives:
        data.append({
            "id": drive.id,
            "title": drive.title,
            "description": drive.description,
            "salary": drive.salary,
            "minimum_cgpa": drive.minimum_cgpa,
            "eligibility_branch": drive.eligibility_branch
        })

    return data


@student_bp.route("/apply/<int:drive_id>", methods=["POST"])
@student_required
def apply_drive(drive_id):

    user_id = get_jwt_identity()

    student = Student.query.filter_by(
        user_id=user_id
    ).first()
    
    if not student:
        return {
            "error": "Student not found"
        }, 404
    if student.is_blacklisted:
        return {
            "error": "Student is blacklisted"
    }, 403

    drive = Drive.query.get(drive_id)

    if not drive:
        return {
            "error": "Drive not found"
        }, 404

    existing_application = Application.query.filter_by(
        student_id=student.id,
        drive_id=drive.id
    ).first()

    if existing_application:
        return {
            "error": "Already applied"
        }, 400

    application = Application(
        student_id=student.id,
        drive_id=drive.id
    )

    db.session.add(application)
    db.session.commit()

    return {
        "message": "Application submitted successfully",
        "application_id": application.id
    }, 201


@student_bp.route("/applications")
@student_required
def my_applications():

    user_id = get_jwt_identity()

    student = Student.query.filter_by(
        user_id=user_id
    ).first()

    applications = Application.query.filter_by(
        student_id=student.id
    ).all()

    data = []

    for application in applications:

        drive = Drive.query.get(
            application.drive_id
        )

        data.append({
            "application_id": application.id,
            "drive_title": drive.title,
            "status": application.status
        })

    return data


@student_bp.route("/placements")
@student_required
def my_placements():

    user_id = get_jwt_identity()

    student = Student.query.filter_by(
        user_id=user_id
    ).first()

    placements = Placement.query.filter_by(
        student_id=student.id
    ).all()

    data = []

    for placement in placements:

        data.append({
            "company_id": placement.company_id,
            "position": placement.position,
            "salary": placement.salary
        })

    return data