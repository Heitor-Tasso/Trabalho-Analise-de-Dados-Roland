# Dashboard routes
from flask import Blueprint, render_template, request, jsonify

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@dashboard_bp.route("/<section>")
def dashboard(section="visao_geral"):
    """Dashboard route with section navigation"""
    return render_template("dashboard/index.html", section=section)

@dashboard_bp.route("/get_charts/<section>")
def get_charts(section):
    """API to get chart data for a specific section"""
    # Implementation will be migrated from app.py
    pass
