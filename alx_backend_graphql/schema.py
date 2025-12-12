import graphene
from crm.schema import CRMQuery   # or from .crm.schema depending on your structure

class Query(CRMQuery, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
