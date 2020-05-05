from fastapi import FastAPI

from models.user import User
from controllers.user import create_user
from routes import auth, excursion, object, statistics, user, track
from utils.auth import get_hash_password

app = FastAPI(title="Excursion-Service",
              description="This service provides paid audio tours",
              version="1", )

admin = User(email='admin@email.ru', hash_password=get_hash_password('AdminPassword_1'), name='Admin', role='admin',
             is_active=True)
create_user(admin)

app.include_router(auth.router)
app.include_router(user.router, prefix='/user')
app.include_router(excursion.router, prefix='/excursion')
app.include_router(track.router, prefix='/track')
app.include_router(statistics.router, prefix='/statistics')
app.include_router(object.router, prefix='/object')
