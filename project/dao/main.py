from typing import Optional, List

from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc
from werkzeug.exceptions import NotFound

from project.dao.base import BaseDAO, T
from project.dao.models import Genre, Movie, Director, User


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie

    def get_all_order_by(self, filter: Optional[str] =None, page: Optional[int] = None) -> List[T]:
        """
        достает все фильмы с фильтрацией по годам в зависимости от статуса
        :param filter:
        :param page:
        :return:
        """
        stmt: BaseQuery = self._db_session.query(self.__model__)

        if filter == 'new': #если есть статус нью то делаем обратную сортировку по годам
            stmt = stmt.order_by(desc(self.__model__.year))

        else:
            stmt = stmt.order_by(self.__model__.year)

        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()


class UsersDAO(BaseDAO[User]):
    __model__ = User

    def create_user(self, email, password):
        """
        создает пользователя
        :param email:
        :param password:
        :return:
        """
        user = User(email=email,
                    password=password)

        try:
            self._db_session.add(user)
            self._db_session.commit()
            print("Пользователь успешно создан")
            return user
        except Exception as e:
            self._db_session.rollback()
            print(e)

    def get_user_by_email(self, email):
        """
        выбирает пользователя по email
        :param email:
        :return:
        """
        return self._db_session.query(self.__model__).filter(self.__model__.email == email).one()

    def update_user(self, data, email):
        """
        обновляет данные пользователя
        :param email:
        :return:
        """
        try:
            self._db_session.query(self.__model__).filter(self.__model__.email == email).update(data)
            self._db_session.commit()
            print ("Пользователь успешно обновлен")
        except Exception as e:
            print("Ошибка обновления пользователя")
            print(e)
            self._db_session.rollback()



