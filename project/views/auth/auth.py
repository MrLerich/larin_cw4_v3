from flask import request
from flask_restx import Namespace, Resource

from project.container import user_service

api: Namespace = Namespace('auth', description="Users Authentication")


@api.route('/register/')
class RegisterUserView(Resource):
    def post(self):
        """
        создает нового пользователя
        :return:
        """
        data = request.json

        if data.get("email") and data.get("password"):
            user_service.create_user(email=data.get("email"),
                                     password=data.get("password"))
            return f"Создан пользователь со следующими данными: {data['email']}"
        else:
            return "Пользователя не удалось создать", 401


@api.route('/login/')
class LoginView(Resource):
    def post(self):
        """
        логин пользователя. проходит аутентификацию пользователя возвращает access_token refresh_token
        :return:
        """
        data = request.json

        if data.get("email") and data.get("password"):
            return user_service.check(email=data.get("email"),
                                               password=data.get("password")), 200
        else:
            return "Пользователя не удалось создать", 401

    def put(self):
        """
        обновляет токены
        :return:
        """
        data = request.json

        if data.get("access_token") and data.get("refresh_token"):
            return user_service.update_token(access_token=data.get("access_token"),
                                             refresh_token=data.get("refresh_token")), 200
        else:
            return "Токены не удалось обновить", 401
