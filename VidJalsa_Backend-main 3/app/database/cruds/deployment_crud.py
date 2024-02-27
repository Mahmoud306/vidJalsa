from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database.database import AbstractDatabase
from app.database.models.models import Deployments
from app.database.cruds.crud_interface import ICRUD


class DeploymentCRUD(ICRUD):
    def __init__(self, db: AbstractDatabase):
        """
        Initialize the DeploymentCRUD class.

        Args:
        - db: An instance of AbstractDatabase.

        Returns:
        - None
        """
        self.db = db

    def add(self, deployment_name: str, deployment_video: str, user_id: int, blog_id: int) -> Deployments:
        """
        Add a new deployment to the database.

        Args:
        - deployment_name: The name of the deployment.
        - deployment_video: The video of the deployment.
        - user_id: The ID of the user associated with the deployment.
        - blog_id: The ID of the blog associated with the deployment.

        Returns:
        - The newly created Deployments object.
        """
        session: Session = self.db.get_session()
        new_deployment = Deployments(deployment_name=deployment_name, deployment_video=deployment_video, user_id=user_id, blog_id=blog_id)
        try:
            session.add(new_deployment)
            session.commit()
            return new_deployment
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            self.db.close_session(session)

    def get(self, deployment_id: int) -> Deployments:
        """
        Get a deployment from the database by its ID.

        Args:
        - deployment_id: The ID of the deployment.

        Returns:
        - The Deployments object with the specified ID.
        """
        session: Session = self.db.get_session()
        try:
            deployment = session.query(Deployments).filter(Deployments.id == deployment_id).first()
            return deployment
        except SQLAlchemyError as e:
            raise e
        finally:
            self.db.close_session(session)

    def update(self, deployment_id: int, **kwargs) -> Deployments:
        """
        Update a deployment in the database.

        Args:
        - deployment_id: The ID of the deployment.
        - kwargs: Keyword arguments representing the fields to be updated.

        Returns:
        - The updated Deployments object.
        """
        session: Session = self.db.get_session()
        try:
            deployment = session.query(Deployments).filter(Deployments.id == deployment_id).first()
            if deployment:
                for key, value in kwargs.items():
                    setattr(deployment, key, value)
                session.commit()
                return deployment
            return None
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            self.db.close_session(session)

    def delete(self, deployment_id: int) -> bool:
        """
        Delete a deployment from the database.

        Args:
        - deployment_id: The ID of the deployment.

        Returns:
        - True if the deployment was successfully deleted, False otherwise.
        """
        session: Session = self.db.get_session()
        try:
            deployment = session.query(Deployments).filter(Deployments.id == deployment_id).first()
            if deployment:
                session.delete(deployment)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            self.db.close_session(session)
