from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiosmtplib import SMTP

from core.config import config, logger
from senders.base import BaseNotificationSender
from senders.model import WelcomeEmailPosting
from utils import messages as msg


class SmartEmailSender(BaseNotificationSender):

    def __init__(
              self,
              posting,
              template_id: str = 'email_confirmation',
    ):
        self.posting = WelcomeEmailPosting.parse_raw(posting)
        self.template_id = template_id

    async def send(self) -> None:
        await self.check_permit(checkers=('deadline', 'not_night'))

        await self.send_with_smtp(to=self.posting.user.email)
        logger.info(msg.email_sent, self.posting.user.email)

    async def send_with_smtp(
              self,
              to: str,
              subject: str | None = None,
    ):
        if subject is None:
            subject = msg.email_confirm_subject
        message = MIMEMultipart("alternative")
        message["From"] = config.smtp_from
        message["To"] = to
        message["Subject"] = subject

        message.attach(MIMEText("hello", "plain", "utf-8"))
        message.attach(MIMEText("<html><body><h1>Hello</h1></body></html>", "html", "utf-8"))
        smtp_client = SMTP(
            hostname=config.smtp_host,
            port=config.smtp_port,
            username=config.smtp_username,
            password=config.smtp_password,
        )
        await smtp_client.connect()
        await smtp_client.send_message(message)
        await smtp_client.quit()
