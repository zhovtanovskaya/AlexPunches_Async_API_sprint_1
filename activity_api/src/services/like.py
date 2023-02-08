from .base import ReactionService
from .models.user_content.likes import Like


class LikeService(ReactionService):

    user_content_type = Like
