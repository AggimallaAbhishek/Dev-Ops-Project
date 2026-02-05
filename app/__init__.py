import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    db_user = os.getenv("DB_USER", "app")
    db_password = os.getenv("DB_PASSWORD", "app_password")
    db_host = os.getenv("DB_HOST", "db")
    db_port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME", "student_results")

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}

    db.init_app(app)

    from app.models import StudentResult

    @app.get("/")
    def health():
        return {"status": "ok"}

    @app.get("/results")
    def list_results():
        results = StudentResult.query.order_by(StudentResult.id.desc()).all()
        return jsonify([r.to_dict() for r in results])

    @app.post("/results")
    def create_result():
        data = request.get_json(silent=True) or {}
        required = ["student_name", "subject", "score"]
        missing = [k for k in required if k not in data]
        if missing:
            return {"error": f"Missing fields: {', '.join(missing)}"}, 400

        result = StudentResult(
            student_name=data["student_name"],
            subject=data["subject"],
            score=int(data["score"]),
        )
        db.session.add(result)
        db.session.commit()
        return result.to_dict(), 201

    @app.get("/results/<int:result_id>")
    def get_result(result_id: int):
        result = StudentResult.query.get_or_404(result_id)
        return result.to_dict()

    return app
