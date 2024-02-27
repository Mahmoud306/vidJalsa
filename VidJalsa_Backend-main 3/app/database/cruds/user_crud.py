# userCrud.py
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database.database import AbstractDatabase
from app.database.models.models import User
from app.database.cruds.crud_interface import ICRUD


class UserCRUD(ICRUD):
    def __init__(self, db: AbstractDatabase):
        self.db = db

    def add(self, username: str, password_hash: str) -> User:
        session: Session = self.db.get_session()
        new_user = User(username=username, password_hash=password_hash)
        try:
            session.add(new_user)
            session.commit()
            return new_user
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            self.db.close_session(session)

    def get(self, user_id: int) -> User:
        session: Session = self.db.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            return user
        except SQLAlchemyError as e:
            raise e
        finally:
            self.db.close_session(session)

    def update(self, user_id: int, **kwargs) -> User:
        session: Session = self.db.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                for key, value in kwargs.items():
                    setattr(user, key, value)
                session.commit()
                return user
            return None
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            self.db.close_session(session)

    def delete(self, user_id: int) -> bool:
        session: Session = self.db.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                session.delete(user)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            self.db.close_session(session)
