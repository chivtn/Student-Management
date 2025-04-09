from StudentManagementApp import db
from StudentManagementApp.models import Regulation

def update_regulation(name, value):
    regulation = Regulation.query.filter_by(name_regulations=name).first()
    if regulation:
        regulation.value_regulations = value
    else:
        regulation = Regulation(name_regulations=name, value_regulations=value)
        db.session.add(regulation)
    db.session.commit()

def get_regulation_value(name):
    regulation = Regulation.query.filter_by(name_regulations=name).first()
    return regulation.value_regulations if regulation else None