from datetime import datetime
from zoneinfo import ZoneInfo

import senders.exceptions as sender_exc
from core.config import logger
from senders.posting_model import PostingBaseModel
from utils import messages as msg
from utils.helpers import is_night


class BaseNotificationSender:
    """Базовый класс отправлятеля нотификаций."""

    def __init__(self):
        """При ините получаем и валидируем даные сообщения на корректность.

        Дочерние классы обязаны реализовать у себя def __init__().
        """
        raise NotImplementedError(msg.needs_method)

    def send(self, posting: PostingBaseModel):
        """Отправить сообщение.

        Обязательно для реализации в дочерних классах.
        """
        if not posting.is_ready():
            return
        raise NotImplementedError(msg.needs_method)
