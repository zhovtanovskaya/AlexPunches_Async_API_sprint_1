from .base import ReactionService
from .models.user_content.ratings import Rating


class RatingService(ReactionService):

    user_content_type = Rating
