// Посчитать средний рейтинг фильма.
db.reactions.aggregate([
    { $match: {"target_type": "movie", "type": "rating"} },
    {
        $group: {
            _id: "$target_id", avgRatings: { $avg : "$value" }, totalRatings: { $count : { } }
        }
    },
    { $sort: { avgRatings: -1 } }
])
// Посчитать количество лайков у ревью на фильм.
db.reactions.aggregate([
    { $match: {"target_type": "review", "type": "like"} },
    {
        $group: {
            _id: "$target_id", totalLikes: { $count : { } }
        }
    },
    { $sort: { totalLikes: -1 } }
])
db.reactions.aggregate([
    { $match: {
        $or: {"target_type": ["review", "like", "rating"] }
    },
    {
        $group: {
            _id: "$target_id", totalLikes: { $avg : "$value" }
        }
    },
    { $sort: { totalLikes: -1 } }
])
// Получить все реакции на конкретное ревью.
db.reactions.find(
    {
        "target_type": "review",
        "target_id": ObjectId("63d0c92bf5eb85d9a10bd8ac"),
    }
)
// Получить все реакции на конкретный фильм.
db.reactions.find(
    {
        "target_type": "movie",
        "target_id": "6fdcc8ca-9c6f-11ed-9682-7831c1bc31e4",
    }
)
// Найти конкретную реакцию. В этом случае -- ревью.
db.reactions.find({
    _id: ObjectId("63d0c92bf5eb85d9a10bd8ac"),
})
// Вот этот запрос не возвращает ничего. Хотя выше
// запрос возвращает объект по этому _id.
db.reactions.find({
  $or: [
      {_id: ObjectId("63d0c92bf5eb85d9a10bd8ac")},
      {_id: ObjectId("6fdcc8ca-9c6f-11ed-9682-7831c1bc31e4")},
  ],
})
db.reactions.find({
  $or: [
      {type: "review"},
      {type: "like"},
  ],
})