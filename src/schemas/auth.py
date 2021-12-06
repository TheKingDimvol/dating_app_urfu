from pydantic import BaseModel


class UserCredentials(BaseModel):
    phone: str
    password: str


class TokenData(BaseModel):
    access_token: str
    token_type: str = 'bearer'
