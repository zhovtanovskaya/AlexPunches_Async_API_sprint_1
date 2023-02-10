from src.services.ugc.base import ReactionService
from src.services.ugc.models.likes import Like


class LikeService(ReactionService):

    user_content_type = Like
