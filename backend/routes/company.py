from flask import Blueprint, request

from flask_jwt_extended import get_jwt_identity

from utils.decorators import company_required

from extensions import db

from models import (
    User,
    Company,
    Drive,
    Application,
    Student,
    Placement
)

company_bp = Blueprint(
    "company",
    __name__
)


@company_bp.route("/dashboard")
@company_required
def dashboard():

    return {
        "message": "Welcome Company"
    }


@company_bp.route("/drives", methods=["POST"])
@company_required
def create_drive():

    user_id = get_jwt_identity()

    company = Company.query.filter_by(
        user_id=user_id
    ).first()

    if not company:
        return {
            "error": "Company not found"
        }, 404

    if company.approval_status != "APPROVED":
        return {
            "error": "Company not approved"
        }, 403

    data = request.get_json()

    drive = Drive(
        company_id=company.id,
        title=data.get("title"),
        description=data.get("description"),
        salary=data.get("salary"),
        required_skills=data.get("required_skills"),
        eligibility_branch=data.get("eligibility_branch"),
        minimum_cgpa=data.get("minimum_cgpa"),
        eligible_year=data.get("eligible_year")
    )

    db.session.add(drive)
    db.session.commit()

    return {
        "message": "Drive created successfully",
        "drive_id": drive.id
    }, 201
@company_bp.route("/drives", methods=["GET"])
@company_required
def get_drives():

    user_id = get_jwt_identity()

    company = Company.query.filter_by(
        user_id=user_id
    ).first()

    if not company:
        return {
            "error": "Company not found"
        }, 404

    drives = Drive.query.filter_by(
        company_id=company.id
    ).all()

    data = []

    for drive in drives:
        data.append({
            "id": drive.id,
            "title": drive.title,
            "description": drive.description,
            "salary": drive.salary,
            "status": drive.status
        })

    return data
@company_bp.route("/applications")
@company_required
def get_applications():

    user_id = get_jwt_identity()

    company = Company.query.filter_by(
        user_id=user_id
    ).first()

    drives = Drive.query.filter_by(
        company_id=company.id
    ).all()

    data = []

    for drive in drives:

        applications = Application.query.filter_by(
            drive_id=drive.id
        ).all()

        for application in applications:

            student = Student.query.get(
                application.student_id
            )

            data.append({
                "application_id": application.id,
                "drive_title": drive.title,
                "student_name": student.name,
                "register_number": student.register_number,
                "status": application.status
            })

    return data
@company_bp.route("/application/<int:application_id>/shortlist", methods=["PUT"])
@company_required
def shortlist_application(application_id):

    application = Application.query.get(application_id)

    if not application:
        return {
            "error": "Application not found"
        }, 404

    application.status = "SHORTLISTED"

    db.session.commit()

    return {
        "message": "Application shortlisted"
    }
@company_bp.route("/application/<int:application_id>/reject", methods=["PUT"])
@company_required
def reject_application(application_id):

    application = Application.query.get(application_id)

    if not application:
        return {
            "error": "Application not found"
        }, 404

    application.status = "REJECTED"

    db.session.commit()

    return {
        "message": "Application rejected"
    }
@company_bp.route("/application/<int:application_id>/select", methods=["PUT"])
@company_required
def select_application(application_id):

    application = Application.query.get(application_id)

    if not application:
        return {
            "error": "Application not found"
        }, 404

    application.status = "SELECTED"

    drive = Drive.query.get(
        application.drive_id
    )

    placement = Placement(
        student_id=application.student_id,
        company_id=drive.company_id,
        position=drive.title,
        salary=drive.salary
    )

    db.session.add(placement)
    db.session.commit()

    return {
        "message": "Candidate selected successfully"
    }