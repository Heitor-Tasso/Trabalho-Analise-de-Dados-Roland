# API routes
from flask import Blueprint, jsonify

api_bp = Blueprint("api", __name__)

@api_bp.route("/version")
def version():
    """Return app version info"""
    return jsonify({
        "app": "Análise Socioeconômica FATEC",
        "version": "2.0.0",
        "visualization_library": "Highcharts",
        "framework": "Flask"
    })
