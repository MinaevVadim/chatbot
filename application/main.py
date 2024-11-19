from fastapi import FastAPI
from routers.habits import router as habit_router
from routers.users import router as user_router
from routers.tokens import router as token_router


app = FastAPI()

app.include_router(habit_router)
app.include_router(user_router)
app.include_router(token_router)
