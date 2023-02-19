from datetime import datetime
from zoneinfo import ZoneInfo

import senders.exceptions as sender_exc
from core.config import logger
from senders.posting_model import PostingBaseModel
from utils import messages as msg
from utils.helpers import is_it_hight


class BaseNotificationSender:
    """Базовый класс отправлятеля нотификаций."""

    def __init__(self, posting: PostingBaseModel):
        """При ините получаем и валидируем даные сообщения на корректность.

        Дочерние классы обязаны реализовать у себя def __init__().
        """
        self.posting = posting
        raise NotImplementedError(msg.needs_method)

    def send(self):
        """Отправить сообщение.

        Обязательно для реализации в дочерних классах.
        """
        self.check_permit(checkers=('deadline',))
        raise NotImplementedError(msg.needs_method)

    def check_permit(
              self,
              checkers: tuple = ('deadline', 'not_night'),
    ) -> bool:
        """Прочекать сообщение на разрешение отправить.

        Список нужных проверок передается в параметре checkers: tuple
        """
        if 'deadline' in checkers and self._check_deadline() is False:
            raise sender_exc.DeadlineNotifyError(msg.deadline_notify_error)
        if 'not_night' in checkers and self._check_not_night() is False:
            logger.info(msg.timeofday_notify_error)
            raise sender_exc.TimeOfDayNotifyError(msg.timeofday_notify_error)
        return True

    def _check_deadline(self):
        """Проверить на дедлайн."""
        return self.posting.deadline > datetime.now()

    def _check_not_night(self):
        """Проверить что сейчас не ночь. Учесть часовой пояс получателя."""
        user_tz = ZoneInfo(self.posting.user_info.timezone)
        return not is_it_hight(datetime.now(tz=user_tz))
