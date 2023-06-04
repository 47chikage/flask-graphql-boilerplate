from models import db,app,Person
from sqlalchemy import text

with app.app_context():
    result = db.session.execute(text('select * from person')).fetchall()

print(result)
