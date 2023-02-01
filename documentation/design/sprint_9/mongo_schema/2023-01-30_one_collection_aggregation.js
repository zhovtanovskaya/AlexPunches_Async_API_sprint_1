use ugc

// Посчитать лайки-дизлайки у ревью.
db.reactions.aggregate([
    {
        $match: {
            target_id: ObjectId("63d0c92bf5eb85d9a10bd8ac"),
            target_type: "review",
        },
    },
    {
        $project: {
            likes: { $cond: [ { $eq: [ "$value", 10 ] }, 1, 0 ] },
            dislikes: { $cond: [ { $eq: [ "$value", 0 ] }, 1, 0 ] },
        }
    },
    {
        $group: {
            _id: "target_id",
            likes: { $sum: "$likes" },
            dislikes: { $sum: "$dislikes" },
        }
    }
])

// Получить ревью, упорядоченные по дате добавления
// и лайкам-дизлайкам.
db.reactions.aggregate([
    { $match: { target_type: "review", type: "like" } },
    // На выходе этого этапа список лайков на ревью вида:
    // { _id: <like_id>, created_at: <like_created_at>, user_id, target_id: <review_id>, target_type, type, value }
    {
        $project: {
            review_id: "$target_id",
            created_at: "$created_at",
            like: { $cond: [ { $eq: [ "$value", 10 ] }, 1, 0 ] },
            dislike: { $cond : [ { $eq: [ "$value", 0 ] }, 1, 0 ] },
        }
    },
    // На выходе список таких документов:
    // { _id: <like_id>, review_id, like: 1, dislike: 0 },
    {
        $group: {
            _id: "$review_id",
            min_like_created_at: { $min: "$created_at"},
            total_likes: { $sum: "$like" },
            total_dislikes: { $sum: "$dislike" },
        }
    },
    // { _id: <review_id>, min_like_created_at, total_likes, total_dislikes }
    {
        $project: {
            // Формула вычисления рейтинга:
            //      (2 * total_likes) - total_dislikes ) /
            //      ( now - min_like_created_at )
            rating: {
                $divide: [
                    { $subtract: [ { $multiply: [ 2, "$total_likes"] } , "$total_dislikes" ] },
                    // Вычислить число миллисекунд с самого давнего лайка.
                    { $subtract: ["$$NOW", "$min_like_created_at" ] },
                ]
            },
        },
    },
    // { _id: <review_id>, rating }
    { $sort: { rating: -1 } },
    // Для паджинации.
    // { $skip: 1 },
    // { $limit: 2 },
    // К каждому документу добавить соответствующую рецензию.
    { $lookup: { from: "reactions", localField: "_id", foreignField: "_id", as: "review" } }
    // { _id: <review_id>, rating, review: {} }
])
