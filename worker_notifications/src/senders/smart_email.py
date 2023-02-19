from datetime import datetime

from senders.base_sender import BaseNotificationSender
from senders.posting_model import PostingBaseModel, WelcomeEmailPosting


class SmartEmailSender(BaseNotificationSender):

    def __init__(self, posting):
        super().__init__(posting)
        self.posting = WelcomeEmailPosting.parse_raw(posting)

    def send(self):
        print(self.posting.user_info)
