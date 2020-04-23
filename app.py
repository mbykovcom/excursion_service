from fastapi import FastAPI

from models.user import User
from controllers.user import create_user
from routes import auth, excursion, object, statistics, user
from utils.auth import get_hash_password

app = FastAPI(title="Excursion-Service",
              description="This service provides paid audio tours",
              version="0.1", )

admin = User(email='admin@email.ru', hash_password=get_hash_password('AdminPassword_1'), name='Admin', role='admin',
             is_active=True)
create_user(admin)

app.include_router(auth.router)
app.include_router(user.router, prefix='/user')
app.include_router(excursion.router, prefix='/excursion')
app.include_router(statistics.router, prefix='/statistics')
app.include_router(object.router, prefix='/object')
