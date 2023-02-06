from .base import ReactionService
from .models.user_content.bookmarks import Bookmark


class BookmarkService(ReactionService):

    user_content_type = Bookmark
