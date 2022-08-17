from flask import request
from flask_restx import Namespace, Resource

from project.container import user_service

api = Namespace('user')

@api.route("/")
class UsersView(Resource):
    @api.marshal_with(user, as_list=True,code=200,description="OK")
    def get(self):
        """
        получает пользователя
        :return:
        """
        token = request.headers["Authorization"].split("Bearer ")[-1]
        return user_service.get_user_by_token(token)

    def patch(self):

