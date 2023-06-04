from flask_graphql import GraphQLView
from graphene import ObjectType, String, Schema,List,ID,Date
from utils.models import Person,db
from sqlalchemy import text
import json
db.JSON_SERIALIZER = json.dumps

#graphql models
class PersonType(ObjectType):
    username=String()
    role=String()

class Query(ObjectType):
    persons=List(PersonType)

    def resolve_persons(self, info):
        query=text("select username,role from person ")
        result = db.session.execute(query)
        return result


schema = Schema(query=Query)