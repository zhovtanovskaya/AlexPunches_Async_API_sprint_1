from .base import ReactionService
from .models.user_content.reviews import Review

PIPELINE = [
    {'$match':  {'target_type':  'review', 'type':  'like'}},
    # На выходе этого этапа список лайков на ревью.
    {
        '$project':  {
            'review_id':  '$target_id',
            'created_at':  '$created_at',
            'like': {
                '$cond': {'if': {'$eq': ['$value', 10]}, 'then': 1, 'else': 0},
            },
            'dislike': {
                '$cond': {'if': {'$eq': ['$value', 0]}, 'then': 1, 'else': 0},
            },
        },
    },
    # На выходе список таких документов':
    # {_id:  <like_id>, review_id, like:  1, dislike:  0},
    {
        '$group':  {
            '_id':  '$review_id',
            'min_like_created_at':  {'$min':  '$created_at'},
            'total_likes':  {'$sum':  '$like'},
            'total_dislikes':  {'$sum':  '$dislike'},
        },
    },
    # {_id:  <review_id>, min_like_created_at, total_likes, total_dislikes}
    {
        '$project':  {
            # Формула вычисления рейтинга':
            #      (2 * total_likes) - total_dislikes ) /
            #      (now - min_like_created_at)
            'rating':  {
                '$divide':  [
                    {
                        '$subtract':  [
                            {'$multiply':  [2, '$total_likes']},
                            '$total_dislikes',
                        ],
                    },
                    # Вычислить число миллисекунд с самого давнего лайка.
                    {'$subtract':  ['$$NOW', '$min_like_created_at']},
                ],
            },
        },
    },
    # {_id: <review_id>, rating}
    {'$sort':  {'rating': -1}},
    # Для паджинации.
    # {'$skip':  1},
    # {'$limit':  2},
    # К каждому документу добавить соответствующую рецензию.
    {
        '$lookup':  {
            'from':  'reactions',
            'localField':  '_id',
            'foreignField':  '_id',
            'as':  'reviews',
        },
    }
    # {_id: <review_id>, rating, review:  [{}]}
]


class ReviewService(ReactionService):

    user_content_type = Review

    async def get_all(self) -> Review:
        result = self.collection.aggregate(PIPELINE)
        async for doc in result:
            # doc выглядит как {_id: <review_id>, rating, reviews: [{}]}.
            # Поле reviews всегда содержит список из одного
            # ревью.  И это ревью с _id равным doc['_id'].
            yield self.to_obj(doc['reviews'][0])
