from typing import Optional, List

from project.dao import UsersDAO
from project.exceptions import ItemNotFound
from project.dao.models import User
from project.tools.security import update_token, generate_token, get_data_by_token, generate_password_hash


class UsersService:
    def __init__(self, dao: UsersDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> User:
        if user := self.dao.get_by_id(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None) -> List[User]:
        return self.dao.get_all(page=page)

    def create_user(self, email, password):
        """
        создает пользователя
        :param email:
        :param password:
        :return:
        """
        return self.dao.create_user(email=email, password=generate_password_hash(password))

    def get_user_by_email(self, email):
        """
        выбирает пользователя по email
        :param email:
        :return:
        """
        return self.dao.get_user_by_email(email=email)

    def check(self, email, password):
        """
        проверяет валидность
        :param email:
        :param password:
        :return:
        """
        user = self.get_user_by_email(email)
        return generate_token(email=email, password=password, password_hash=user.password)

    def update_token(self, access_token, refresh_token):
        """
        обновляет токены
        :param access_token:
        :param refresh_token:
        :return:
        """
        return update_token(refresh_token=refresh_token)

    def get_user_by_token(self, token):
        """
        из токена вынимает сведения о пользователе
        :param token:
        :return:
        """
        data = get_data_by_token(token)
        if data:
            user = self.get_user_by_email(data.get("email"))
            user.password = "******"                        #прячу пароль чтобы явно не показывался при выводе
            return user

    def update_user(self, data, token):
        user = get_data_by_token(token)

        if user:
            self.dao.update_user(data=data, email=user.get("email"))


            user_data = self.get_user_by_email(user.get("email"))
            user_data.password = "******"
            return user_data


    def update_password(self, data, token):
        """
        обновляет пароль пользователя
        :param data:
        :param token:
        :return:
        """
        user = get_data_by_token(token)

        if user:
            self.dao.update_user(
                data={
                    "password": generate_password_hash(data.get("password_2"))
                },
                email=user.get("email")
            )

            user_data = self.get_user_by_email(user.get("email"))
            user_data.password = "******"
            return user_data













