from flask import Blueprint, request, jsonify

from extensions import db
from models import User, Student
from models import User, Student, Company
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from extensions import db
from models import User, Student, Company
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route("/health")
def health():
    return {
        "message": "Auth Blueprint Working"
    }


@auth_bp.route("/register/student", methods=["POST"])
def register_student():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    name = data.get("name")
    register_number = data.get("register_number")
    branch = data.get("branch")
    cgpa = data.get("cgpa")
    year = data.get("year")
    phone = data.get("phone")

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:
        return jsonify({
            "error": "Email already exists"
        }), 400

    user = User(
        email=email,
        role="STUDENT"
    )

    user.set_password(password)

    db.session.add(user)
    db.session.flush()

    student = Student(
        user_id=user.id,
        name=name,
        register_number=register_number,
        branch=branch,
        cgpa=cgpa,
        year=year,
        phone=phone
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({
        "message": "Student registered successfully",
        "student_id": student.id
    }), 201
@auth_bp.route("/register/company", methods=["POST"])
def register_company():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    company_name = data.get("company_name")
    industry = data.get("industry")
    location = data.get("location")
    website = data.get("website")
    hr_contact = data.get("hr_contact")

    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:
        return jsonify({
            "error": "Email already exists"
        }), 400

    user = User(
        email=email,
        role="COMPANY"
    )

    user.set_password(password)

    db.session.add(user)
    db.session.flush()

    company = Company(
        user_id=user.id,
        company_name=company_name,
        industry=industry,
        location=location,
        website=website,
        hr_contact=hr_contact,
        approval_status="PENDING"
    )

    db.session.add(company)
    db.session.commit()

    return jsonify({
        "message": "Company registered successfully",
        "company_id": company.id,
        "status": company.approval_status
    }), 201
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:
        return jsonify({
            "error": "Invalid credentials"
        }), 401

    if not user.check_password(password):
        return jsonify({
            "error": "Invalid credentials"
        }), 401

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role
        }
    )

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "role": user.role,
        "user_id": user.id
    }), 200
@auth_bp.route("/me")
@jwt_required()
def me():

    user_id = get_jwt_identity()

    claims = get_jwt()

    return {
        "user_id": user_id,
        "role": claims["role"]
    }