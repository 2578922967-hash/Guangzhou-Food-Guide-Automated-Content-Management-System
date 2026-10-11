"""
API 包初始化。
"""

from __future__ import annotations

from flask import Flask
from flask_cors import CORS

from .routes import reports, restaurants, statistics, templates


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(restaurants.bp, url_prefix="/api/restaurants")
    app.register_blueprint(templates.bp, url_prefix="/api/templates")
    app.register_blueprint(reports.bp, url_prefix="/api/reports")
    app.register_blueprint(statistics.bp, url_prefix="/api/statistics")

    @app.route("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


