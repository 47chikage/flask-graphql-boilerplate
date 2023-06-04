from models import *
from gql_utils import *

#populate your database after creating it with models
#dont forget to delete my own records
with app.app_context():
    person1=Person(username='habib',password='ilovecheese',role='admin')
    person2=Person(username='habib2',password='yesyesyall',role='whatever role')
    db.session.add_all([person1,person2])
    db.session.commit()