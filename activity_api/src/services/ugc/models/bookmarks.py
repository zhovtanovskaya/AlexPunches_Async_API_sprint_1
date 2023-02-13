from src.services.ugc.models.base import ContentType, MovieReaction


class Bookmark(MovieReaction):
    type: ContentType = ContentType.BOOKMARK
