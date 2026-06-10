from flask import Blueprint

from utils.decorators import admin_required
from extensions import db
import csv
import os
import redis
import json

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

from flask import send_file

from models import (
    User,
    Student,
    Company,
    Drive,
    Application,
    Placement
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
@admin_bp.route("/drives")
@admin_required
def get_drives():

    drives = Drive.query.all()

    data = []

    for drive in drives:

        company = Company.query.get(
            drive.company_id
        )

        data.append({
            "id": drive.id,
            "title": drive.title,
            "company_name": company.company_name,
            "salary": drive.salary,
            "status": drive.status
        })

    return data


@admin_bp.route("/students")
@admin_required
def get_students():

    students = Student.query.all()

    data = []

    for student in students:

        data.append({
            "id": student.id,
            "name": student.name,
            "register_number": student.register_number,
            "branch": student.branch,
            "cgpa": student.cgpa,
            "is_blacklisted": student.is_blacklisted
        })

    return data


@admin_bp.route("/student/<int:student_id>/blacklist", methods=["PUT"])
@admin_required
def blacklist_student(student_id):

    student = Student.query.get(student_id)

    if not student:
        return {
            "error": "Student not found"
        }, 404

    student.is_blacklisted = True

    db.session.commit()

    return {
        "message": "Student blacklisted successfully"
    }


@admin_bp.route("/student/<int:student_id>/unblacklist", methods=["PUT"])
@admin_required
def unblacklist_student(student_id):

    student = Student.query.get(student_id)

    if not student:
        return {
            "error": "Student not found"
        }, 404

    student.is_blacklisted = False

    db.session.commit()

    return {
        "message": "Student unblacklisted successfully"
    }
@admin_bp.route("/placements")
@admin_required
def get_placements():
    cached = r.get(
        "placements_report"
    )

    if cached:
        return json.loads(cached)

    placements = Placement.query.all()

    data = []

    for placement in placements:

        student = Student.query.get(
            placement.student_id
        )

        company = Company.query.get(
            placement.company_id
        )

        data.append({
            "student_name": student.name,
            "register_number": student.register_number,
            "company_name": company.company_name,
            "position": placement.position,
            "salary": placement.salary
        })

    r.setex(
        "placements_report",
        3600,  
        json.dumps(data)
    )

    return data
@admin_bp.route("/export/placements")
@admin_required
def export_placements():

    placements = Placement.query.all()

    export_path = os.path.join(
        "exports",
        "placements.csv"
    )

    with open(
        export_path,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Student Name",
            "Register Number",
            "Company Name",
            "Position",
            "Salary"
        ])

        for placement in placements:

            student = Student.query.get(
                placement.student_id
            )

            company = Company.query.get(
                placement.company_id
            )

            writer.writerow([
                student.name,
                student.register_number,
                company.company_name,
                placement.position,
                placement.salary
            ])

    return send_file(
        export_path,
        as_attachment=True
    )