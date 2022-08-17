import base64
import calendar
import datetime
import hashlib
from typing import Union

import jwt
from flask import current_app


def __generate_password_digest(password: str) -> bytes:
    """
    генерирует хэш пароля
    :param password:
    :return:
    """
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def generate_password_hash(password: str) -> str:
    """
        генерирует хэш пароля
        :param password:
        :return:
        """
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')


def compare_passwords(password_hash: Union[str, bytes], other_password: str) -> bool:
    """
    сравнивает вводимый пароль с паролем в базе
    :param password_hash: пароль из БД
    :param other_password: пароль вводимый пользователем
    :return:
    """
    return password_hash == generate_password_hash(other_password)


def generate_token(email, password, password_hash, refresh=False):
    if not email:
        return None

    if not refresh:
        if not compare_passwords(password_hash=password_hash, other_password=password):
            return None

    data = {
        "email": email,
        "password": password
    }

    # 30 min for access_token
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config["TOKEN_EXPIRE_MINUTES"])
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data,
                              key=current_app.config["SECRET_KEY"],
                              algorithm=current_app.config["ALGORITHM"])
    # day for refresh_token
    min_day = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config["TOKEN_EXPIRE_DAY"])
    data["exp"] = calendar.timegm(min_day.timetuple())
    refresh_token = jwt.encode(data,
                               key=current_app.config["SECRET_KEY"],
                               algorithm=current_app.config["ALGORITHM"])

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


def update_token(refresh_token):
    """
    обновляет токены
    :param refresh_token:
    :return:
    """
    data = jwt.decode(refresh_token,
                      key=current_app.config["SECRET_KEY"],
                      algorithms=current_app.config["ALGORITHM"])

    email = data.get("email")
    password = data.get("password")

    return generate_token(email=email,
                          password=password,
                          password_hash=None,
                          refresh=True)


def get_data_by_token(refresh_token):
    """
    получает данные по токену
    :param refresh_token:
    :return:
    """
    data = jwt.decode(refresh_token,
                      key=current_app.config["SECRET_KEY"],
                      algorithms=current_app.config["ALGORITHM"])

    return data


