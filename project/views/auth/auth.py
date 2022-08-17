from flask import request
from flask_restx import Namespace, Resource
from project.container import user_service
from project.setup.api.models import user
from project.setup.api.parsers import page_parser

api = Namespace('auth')

@api.route('/register/')
class RegisterUserView(Resource):
    def post(self):
        """
        создает нового пользователя
        :return:
        """
        data = request.json

        if data.get("email") and data.get("password"):
            return user_service.create_user(email=data.get("email"),
                                            password=data.get("password")), \
                   201,\
                   {"location":f"/users/{user.id}"}
        else:
            return "Пользователя не удалось создать", 401

@api.route('/login'/)
class LoginnView(Resource):
    def post(self):
        """
        логин пользователя. проходит аутентификацию пользователя возвращает access_token refresh_token
        :return:
        """
        data = request.json

        if data.get("email") and data.get("password"):
            return user_service.create_user(email=data.get("email"),
                                            password=data.get("password")), \
                   201, \
                   {"location": f"/users/{user.id}"}
        else:
            return "Пользователя не удалось создать", 401

