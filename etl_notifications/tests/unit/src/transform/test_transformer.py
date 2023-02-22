import unittest

from src.transform.users import UserSignedUpTransformer
from tests.unit.src.extract.fixtures.events import UserSignedUpEvent


class TransformTestCase(unittest.IsolatedAsyncioTestCase):

    async def test(self):
        event = UserSignedUpEvent()
        transformer = UserSignedUpTransformer()
        posting = await anext(transformer.make_postings(event))
        self.assertEqual(event.details.email, posting.user.email)
