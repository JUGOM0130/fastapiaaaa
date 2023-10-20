"""
Auth
https://scrapbox.io/PythonOsaka/FastAPI%E3%81%A7Web%E3%82%B5%E3%83%BC%E3%83%93%E3%82%B9%E3%82%92%E4%BF%9D%E8%AD%B7%E3%81%97%E3%81%A6%E3%81%BF%E3%82%8B
"""

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi_login.fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException


SECRET = "8c135d24ed30d57f770967295653cc48adf3003ceedc95be"

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

manager = LoginManager(SECRET, token_url='/auth/token')

fake_db = {'freddie@example.com': {'password': 'queen'}}



@manager.user_loader
def load_user(email: str):
    print("load_user")
    user = fake_db.get(email)
    print(user)

@app.post('/auth/token')
def login(data = Depends()):
    print("login")

    email = data.username
    password = data.password

    user = load_user(email)
    if not user:
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}

@app.get("/")
def index(user=Depends(manager)):
    print("index")
    return {"hello": "world!!","user":user}

@app.get("/test")
def test():
    print("test")
    return {"test": "world!!"}


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}




if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000,reload=True)