"""Управлять социальными аккаунтами."""
from uuid import UUID

from models.social_account import SocialAccount


class SocialAccountService:
    """Сервис управления социальными аккаунтами."""

    @staticmethod
    def get_or_create_soc_acc(social_id: str,
                              social_name: str,
                              user_id: UUID,
                              ) -> SocialAccount:
        """Получить SocialAccount, если нет, создать."""
        soc_acc = SocialAccount.query.filter_by(
            social_id=social_id, social_name=social_name).first()
        if not soc_acc:
            soc_acc = SocialAccount(
                social_id=social_id, social_name=social_name, user_id=user_id)
            soc_acc.create()
        return soc_acc
