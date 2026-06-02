from flask import Blueprint

from utils.decorators import admin_required
from extensions import db

from models import (
    Student,
    Company,
    Drive,
    Application
)

admin_bp = Blueprint(
    "admin",
    __name__
)


@admin_bp.route("/dashboard")
@admin_required
def dashboard():

    total_students = Student.query.count()

    total_companies = Company.query.count()

    total_drives = Drive.query.count()

    total_applications = Application.query.count()

    return {
        "total_students": total_students,
        "total_companies": total_companies,
        "total_drives": total_drives,
        "total_applications": total_applications
    }
@admin_bp.route("/companies")
@admin_required
def get_companies():

    companies = Company.query.all()

    data = []

    for company in companies:

        data.append({
            "id": company.id,
            "company_name": company.company_name,
            "industry": company.industry,
            "location": company.location,
            "approval_status": company.approval_status
        })

    return data
@admin_bp.route("/company/<int:company_id>/approve", methods=["PUT"])
@admin_required
def approve_company(company_id):

    company = Company.query.get(company_id)

    if not company:
        return {
            "error": "Company not found"
        }, 404

    company.approval_status = "APPROVED"

    db.session.commit()

    return {
        "message": "Company approved successfully"
    }
@admin_bp.route("/company/<int:company_id>/reject", methods=["PUT"])
@admin_required
def reject_company(company_id):

    company = Company.query.get(company_id)

    if not company:
        return {
            "error": "Company not found"
        }, 404

    company.approval_status = "REJECTED"

    db.session.commit()

    return {
        "message": "Company rejected successfully"
    }
@admin_bp.route("/drive/<int:drive_id>/approve", methods=["PUT"])
@admin_required
def approve_drive(drive_id):

    drive = Drive.query.get(drive_id)

    if not drive:
        return {
            "error": "Drive not found"
        }, 404

    drive.status = "APPROVED"

    db.session.commit()

    return {
        "message": "Drive approved successfully"
    }