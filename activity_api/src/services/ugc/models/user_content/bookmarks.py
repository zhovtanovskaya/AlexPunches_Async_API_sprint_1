from .base import ContentType, MovieReaction


class Bookmark(MovieReaction):
    type: ContentType = ContentType.BOOKMARK
