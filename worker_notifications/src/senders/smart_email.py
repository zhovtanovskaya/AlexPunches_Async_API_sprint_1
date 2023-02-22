from core.config import logger
from senders.base import BaseNotificationSender
from senders.model import WelcomeEmailPosting


class SmartEmailSender(BaseNotificationSender):

    def __init__(self, posting):
        self.posting = WelcomeEmailPosting.parse_raw(posting)

    def send(self) -> None:
        self.check_permit(checkers=('deadline', 'not_night'))
        logger.info(self.posting.user_info.name)
