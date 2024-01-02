import jwt
from typing import List
from fastapi import FastAPI, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from app.crud import get_user, get_clients, get_companies, get_user_clients, get_articles, get_client_articles
from app.models.user import TokenRequest, TokenResponse
from app.models.user_client import UserClient
from app.models.client import Client
from app.models.company import Company
from app.models.article import Article
from app.models.client_article import ClientArticle

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/login", response_model=TokenResponse)
def login(user: TokenRequest):
    if validate_credentials(user.username, user.password):
        # Generate a JWT token
        token_data = {"sub": user.username, "scopes": ["me"]}
        token = create_jwt_token(token_data)

        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def validate_credentials(loginname: str, password: str) -> bool:
    # Implement your authentication logic here
    # For example, check if the provided loginname and password match a user in the database
    user = get_user(loginname)
    print(user)
    if user is not None and user['PASSWORD'] == password:
        return user
    return False


def create_jwt_token(token_data: dict) -> str:
    return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)


@app.get("/clients", response_model=List[Client])
def list_clients():
    return get_clients()


@app.get("/companies", response_model=List[Company])
def list_companies(client_id: str = Query(..., description="Client ID to filter companies")):
    return get_companies(client_id)


@app.get("/user-clients", response_model=List[UserClient])
def list_user_clients(loginname: str = Query(..., description="Login name to filter user clients")):
    return get_user_clients(loginname)


@app.get("/articles", response_model=List[Article])
def list_articles():
    return get_articles()


@app.get("/client_articles", response_model=List[ClientArticle])
def list_client_articles():
    return get_client_articles()
