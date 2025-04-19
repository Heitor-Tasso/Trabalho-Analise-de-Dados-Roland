# Upload routes
from flask import Blueprint, render_template, request, redirect, url_for, flash

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/")
def home():
    """Home page with upload form"""
    return render_template("upload/index.html")

@upload_bp.route("/upload", methods=["POST"])
def upload_file():
    """Handle file upload"""
    # Implementation will be migrated from app.py
    pass
