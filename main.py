from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, jwt_auth_users, scraping

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
app.include_router(scraping.router)

