# blogCrud.py
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database.database import AbstractDatabase
from app.database.models.models import Blog
from app.database.cruds.crud_interface import ICRUD

class BlogCRUD(ICRUD):
    """
    A class that provides CRUD operations for the Blog entity.
    """

    def __init__(self, db: AbstractDatabase):
        """
        Initializes a new instance of the BlogCRUD class.

        Args:
            db (AbstractDatabase): The database instance to use for CRUD operations.
        """
        self.db = db

    def add(self, author_id: int, title: str, question: str, paragraphs: list, image_url: str) -> Blog:
        """
        Adds a new blog to the database.

        Args:
            author_id (int): The ID of the author of the blog.
            title (str): The title of the blog.
            question (str): The question associated with the blog.
            paragraphs (list): A list of paragraphs for the blog.

        Returns:
            Blog: The newly created blog object.
        """
        session: Session = self.db.get_session()
        new_blog = Blog(user_id=author_id, title=title, question=question, paragraphs=paragraphs,image_url=image_url)
        session.add(new_blog)
        session.commit()
        print(new_blog.id)
        return new_blog

    def get(self, blog_id: int) -> Blog:
        """
        Retrieves a blog from the database by its ID.

        Args:
            blog_id (int): The ID of the blog to retrieve.

        Returns:
            Blog: The retrieved blog object.
        """
        session: Session = self.db.get_session()
        try:
            blog = session.query(Blog).filter(Blog.id == blog_id).first()
            return blog
        except SQLAlchemyError as e:
            raise e
        finally:
            self.db.close_session(session)

    def update(self, blog_id: int, **kwargs) -> Blog:
        """
        Updates a blog in the database.

        Args:
            blog_id (int): The ID of the blog to update.
            **kwargs: Keyword arguments representing the fields to update.

        Returns:
            Blog: The updated blog object.
        """
        session: Session = self.db.get_session()
        try:
            blog = session.query(Blog).filter(Blog.id == blog_id).first()
            if blog:
                for key, value in kwargs.items():
                    setattr(blog, key, value)
                session.commit()
                return blog
            return None
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            self.db.close_session(session)

    def delete(self, blog_id: int) -> bool:
        """
        Deletes a blog from the database.

        Args:
            blog_id (int): The ID of the blog to delete.

        Returns:
            bool: True if the blog was successfully deleted, False otherwise.
        """
        session: Session = self.db.get_session()
        try:
            blog = session.query(Blog).filter(Blog.id == blog_id).first()
            if blog:
                session.delete(blog)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            self.db.close_session(session)
