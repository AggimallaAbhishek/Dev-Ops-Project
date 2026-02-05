from app import db


class StudentResult(db.Model):
    __tablename__ = "student_results"

    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "student_name": self.student_name,
            "subject": self.subject,
            "score": self.score,
        }
