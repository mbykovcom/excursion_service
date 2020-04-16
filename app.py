from fastapi import FastAPI

from routes import auth, excursion, object, route, statistics, user

app = FastAPI(title="Excursion-Service",
              description="This service provides paid audio tours",
              version="0.1", )

app.include_router(auth.router)
app.include_router(user.router, prefix='/user')
app.include_router(excursion.router, prefix='/excursion')
app.include_router(statistics.router, prefix='/statistics')
app.include_router(route.router, prefix='/route')
app.include_router(object.router, prefix='/object')
