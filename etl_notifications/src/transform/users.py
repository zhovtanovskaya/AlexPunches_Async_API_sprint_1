from datetime import datetime, timedelta
from typing import AsyncIterable

from src.extract.events.users import UserSignedUpEvent
from src.transform.postings.users import UserInfo, WelcomeEmailPosting


class UserSignedUpTransformer:

    async def make_postings(
            self, event: UserSignedUpEvent
    ) -> AsyncIterable[WelcomeEmailPosting]:
        user = UserInfo(name='', last_name='', email=event.details.email)
        deadline = datetime.now() + timedelta(days=1)
        posting = WelcomeEmailPosting(deadline=deadline, user=user)
        yield posting
