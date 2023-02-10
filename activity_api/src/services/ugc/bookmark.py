from src.services.ugc.base import ReactionService
from src.services.ugc.models.bookmarks import Bookmark


class BookmarkService(ReactionService):

    user_content_type = Bookmark
