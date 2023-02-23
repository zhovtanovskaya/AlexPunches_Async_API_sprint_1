import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiosmtplib import SMTP
from jinja2 import Environment, FileSystemLoader

from core.config import config, logger
from senders.base import BaseNotificationSender
from senders.model import WelcomeEmailPosting
from utils import messages as msg


class SmartEmailSender(BaseNotificationSender):

    def __init__(self, posting):
        self.posting = WelcomeEmailPosting.parse_raw(posting)

    async def send(self) -> None:
        await self.check_permit(checkers=('deadline', 'not_night'))
        await self._send_with_smtp()
        logger.info(msg.email_sent, self.posting.user.email)

    async def _send_with_smtp(self) -> None:
        subject = msg.email_confirm_subject
        text = self._render_mail_from_posting()

        message = MIMEMultipart()
        message["From"] = config.smtp_from
        message["To"] = self.posting.user.email
        message["Subject"] = subject

        message.attach(MIMEText(text, "html", "utf-8"))
        smtp_client = SMTP(
            hostname=config.smtp_host,
            port=config.smtp_port,
            username=config.smtp_username,
            password=config.smtp_password,
        )
        await smtp_client.connect()
        await smtp_client.send_message(message)
        await smtp_client.quit()

    def _render_mail_from_posting(self) -> str:
        # шаблоны скорее всего должны управляться админкой, но пока так...
        env = Environment(
            loader=FileSystemLoader(
                '%s/templates/' % os.path.dirname(os.path.dirname(__file__))
            )
        )
        template = env.get_template('email_confirmation.html')
        return template.render(posting=self.posting)
