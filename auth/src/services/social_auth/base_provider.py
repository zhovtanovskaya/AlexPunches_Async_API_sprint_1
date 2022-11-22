"""Базовый класс OAuth 2.0 провайдера."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type
from uuid import UUID

from core.db import db
from models.social_account import SocialAccount


@dataclass()
class SocUser:
    """Дата-класс SocUser.

    social_id: ID юзера в соц.провайдере
    user_id: ID юзера у нас
    """

    social_id: str
    user_id: UUID


class BaseOAuth(ABC):
    """Абстракция для провайдера OAuth 2.0."""

    soc_acc_model: Type[db.Model] = SocialAccount
    social_name: str  # используется как значение social_name в SocialAccount

    @abstractmethod
    def get_oauth_url(self) -> str:
        """Получить url у провайдера, на который отправим юзера."""
        pass

    @abstractmethod
    def auth(self, request_url, data) -> SocUser:
        """Пытаемся авторизоваться.

        :param request_url: url со всеми query параметрами в строке
        :param data: POST данные
        :return: SocUser
        """
        pass
