from app.database import database
from app.database.models.models import *

database_url = "mysql+mysqlconnector://user:password@localhost:3306/vidjalsa"
database_connection = database.SqlAlchemyDatabaseConnection(database_url)

database_connection.Base.metadata.create_all(database_connection.engine)


# from app.database.cruds.user_crud import UserCRUD
# USER_CRUD = UserCRUD(database_connection)
# USER_CRUD.add("hamza","1234")

# from app.Database.Cruds.Deployment_crud import DeploymentCRUD
# Deployment_CRUD =  DeploymentCRUD(database_connection)
# DeploymentCRUD.add(self=Deployment_CRUD,deployment_name="deployment_name", deployment_video="ddd", user_id=1, blog_id=1)
