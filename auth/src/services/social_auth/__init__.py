"""Удобные имрорты из одной точки."""
from .base_provider import BaseOAuth, SocUser
from .google_provider import GoogleOAuthProvider
from .oauth import OAuthService, get_oauth_service

__all__ = [
    'BaseOAuth',
    'SocUser',
    'GoogleOAuthProvider',
    'OAuthService',
    'get_oauth_service',
]
