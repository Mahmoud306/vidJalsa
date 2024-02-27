from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import SqlAlchemyDatabaseConnection

class User(SqlAlchemyDatabaseConnection.Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password_hash = Column(String(255))

    def __repr__(self):
        return f"<User(username='{self.username}', id='{self.id}')>"

class Blog(SqlAlchemyDatabaseConnection.Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    question = Column(String(255), nullable=False)
    paragraphs = Column(JSON, nullable=False)
    image_url = Column(String(1000), nullable=False)

    # Foreign key to associate a blog with a user
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User")

    def __repr__(self):
        return f"<Blog(title='{self.title}', user_id='{self.user_id}')>"


class Deployments(SqlAlchemyDatabaseConnection.Base):
    __tablename__ = 'deployments'
    id = Column(Integer, primary_key=True)
    deployment_name = Column(String(255), nullable=False)
    deployment_video = Column(String(255), nullable=False)

    # Foreign key to associate a deployment with a user
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User")

    # Foreign key to associate a deployment with a blog
    blog_id = Column(Integer, ForeignKey('blogs.id'))
    blog = relationship("Blog")

    def __repr__(self):
        return f"<Deployments(deployment_name='{self.deployment_name}', user_id='{self.user_id}', blog_id='{self.blog_id}')>"
