import jwt
import fitz
from openai import OpenAI
from typing import List
from selenium import webdriver
from fastapi import FastAPI, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from app.crud import get_user, get_clients, get_companies, get_user_clients, get_articles, get_client_articles
from app.models.user import TokenRequest, TokenResponse
from app.models.user_client import UserClient
from app.models.client import Client
from app.models.company import Company
from app.models.article import Article
from app.models.client_article import ClientArticle
from selenium.webdriver.common.by import By

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"


app = FastAPI()

client = OpenAI(
    api_key='',
)

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


@app.post("/generate-summary")
async def generate_summary_from_url(payload: dict):
    # Extract text from the dynamic webpage
    dynamic_webpage_text = extract_text_from_dynamic_webpage(
        payload.get('url'))

    # Generate summary using GPT-3.5-turbo
    summary = generate_summary(dynamic_webpage_text)

    return {"summary": summary}


def generate_summary(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Provide summary of text"},
            {"role": "user", "content": text[:3000]}
        ],
        max_tokens=300,
        temperature=0.5
    )
    return response.choices[0].message.content


def extract_text_from_dynamic_webpage(url):
    try:
        # Set up the selenium webdriver (make sure you have the appropriate webdriver executable installed)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode
        driver = webdriver.Chrome(options=options)

        # Open the webpage and wait for it to load (adjust wait time based on your needs)
        driver.get(url)
        # driver.implicitly_wait(3)

        # Extract text from the dynamic webpage
        # webpage_text = driver.find_element_by_xpath("/html/body").text
        webpage_text = driver.find_element(By.XPATH, "/html/body").text

        return webpage_text
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Failed to fetch content from the dynamic webpage: {str(e)}")
    finally:
        # Close the webdriver
        driver.quit()
