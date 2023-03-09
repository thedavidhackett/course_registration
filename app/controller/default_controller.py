from flask import g
from flask_restful import Api, Resource

class GetUserHandler(Resource):
  def get(self):
    return g.user.view()

def register(api : Api) -> None:
  api.add_resource(GetUserHandler, "/api/get-user")
