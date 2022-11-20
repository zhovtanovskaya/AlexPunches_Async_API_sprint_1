"""Модуль для JWT-авторизации."""

import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


class JWTBearer(HTTPBearer):
    """Проверка заголовка Authorization в HTTP-запросе.

    Методы класса проверяют, что в заголовке авторизации обязательно
    содержится валидный JWT.
    """

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(status_code=403, detail='Invalid authorization code.')
        if not credentials.scheme == 'Bearer':
            raise HTTPException(status_code=403, detail='Invalid authentication scheme.')
        if not self.verify_jwt(credentials.credentials):
            raise HTTPException(status_code=403, detail='Invalid token or expired token.')
        return credentials

    def verify_jwt(self, token: str):
        SECRET_KEY = 'secret'
        ALGORITHM = 'HS256'
        print(token)
        # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg'
        # try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # jwt.exceptions.DecodeError: Not enough segments
        # except (JWTError, ValidationError):
        return True