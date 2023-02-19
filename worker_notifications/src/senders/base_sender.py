import time
from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime
from zoneinfo import ZoneInfo

from core.config import config
from senders.posting_model import PostingBaseModel
from utils.helpers import is_it_hight


class BaseNotificationSender:

    def __init__(self, posting):
        self.posting = PostingBaseModel.parse_raw(posting)

    def check_permit(self) -> bool:
        if self._check_deadline() is False:
            return False
        if self._check_not_night() is False:
            return False
        return True

    def send(self):
        pass

    def _check_deadline(self):
        return self.posting.deadline > datetime.now()

    def _check_not_night(self):
        user_tz = ZoneInfo(self.posting.user_info.timezone)
        return not is_it_hight(datetime.now(tz=user_tz))
