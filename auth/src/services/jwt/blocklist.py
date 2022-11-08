"""Отзыв JWT-токенов."""

from core.redis import jwt_redis_blocklist
from manage import app


@app.jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    """Проверить, что JWT существует в черном списке Redis."""
    jti = jwt_payload['jti']
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None
