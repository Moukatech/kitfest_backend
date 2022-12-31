from typing import Optional
import base64
from datetime import datetime, timedelta
import time

import jwt
from jwt import PyJWTError

from fastapi.openapi.models import SecurityBase as SecurityBaseModel
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel

from starlette.status import HTTP_403_FORBIDDEN
from starlette.requests import Request
from decouple import config 

# SECRET_KEY = config('JWT_SECRET')
# ALGORITHM = config('JWT_ALGORITHM')
SECRET="d36dd95da0cc5bc52fd01513a1dbb4775610cedd9a68ffab815c44f1d0bebede"
ALGORITHM="HS256"

class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        header_authorization: str = request.headers.get("Authorization")
        cookie_authorization: str = request.cookies.get("Authorization")

        header_scheme, header_param = get_authorization_scheme_param(
            header_authorization
        )
        cookie_scheme, cookie_param = get_authorization_scheme_param(
            cookie_authorization
        )

        if header_scheme.lower() == "bearer":
            authorization = True
            scheme = header_scheme
            param = header_param

        elif cookie_scheme.lower() == "bearer":
            authorization = True
            scheme = cookie_scheme
            param = cookie_param

        else:
            authorization = False

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        return param


class BasicAuth(SecurityBase):
    def __init__(self, scheme_name: str = None, auto_error: bool = True):
        self.scheme_name = scheme_name or self.__class__.__name__
        self.model = SecurityBase() 
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "basic":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        return param
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt

def decodeJWT(token):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload if payload["exp"] >= time.time() else None
    except:
        return {"error": "token decode failed"}