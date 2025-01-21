from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from routers import users, jwt_auth_users
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router)
app.include_router(jwt_auth_users.router)



