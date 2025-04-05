# models/score_detail.py
from StudentManagementApp import db
from StudentManagementApp.models.enums import ScoreType

class ScoreDetail(db.Model):
    __tablename__ = 'score_detail'
    id = db.Column(db.Integer, primary_key=True)
    score_sheet_id = db.Column(db.Integer, db.ForeignKey('score_sheet.id'), nullable=False)
    type = db.Column(db.Enum(ScoreType), nullable=False)
    value = db.Column(db.Float, nullable=False)

    score_sheet = db.relationship('ScoreSheet', backref='details')