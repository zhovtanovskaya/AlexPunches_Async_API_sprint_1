// Запросы к схеме документов one_collection_docs.js
// Версия от 2023-01-25.

// Переключиться на тестовую базу данных.
use ugc

// Посчитать среднюю оценку фильма и число оценок у фильмов.
db.reactions.aggregate([
    { $match: {"target_type": "movie", "type": "rating"} },
    {
        $group: {
            _id: "$target_id", avgRatings: { $avg : "$value" }, totalRatings: { $count : { } }
        }
    },
    { $sort: { avgRatings: -1 } }
])
// Посчитать количество рецензий на фильм.
db.reactions.aggregate([
    {
        $match: {
            "target_type": "movie",
            "type": "review",
            "target_id": "6fdcc8ca-9c6f-11ed-9682-7831c1bc31e4",
        }
    },
    {
        $group: {
            _id: "$value", count: { $count : { } }
        }
    },
])
// Получить реакции конкретного пользователя.
db.reactions.aggregate([
    {
        $match: {
            $or: [{type: "rating"}, {type: "review"},],
            "user_id": "60bf29d4-9c6f-11ed-9400-7831c1bc31e4",
            "target_id": "6fdcc8ca-9c6f-11ed-9682-7831c1bc31e4",
        }
    },
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
// Вот этот запрос выбрасывает ошибку.  Потому что
// у UUID формат не подходит для ObjectId.
db.reactions.find({
  $or: [
      {_id: ObjectId("63d0c92bf5eb85d9a10bd8ac")},
      {_id: ObjectId("6fdcc8ca-9c6f-11ed-9682-7831c1bc31e4")},
  ],
})
// Выбрать ревью или лайки.
db.reactions.find({
  $or: [
      {type: "review"},
      {type: "like"},
  ],
})
// Получить положительные рецензии на конкретный фильм.
db.reactions.find(
    {
        target_type: "movie",
        type: "review",
        target_id: "6fdcc8ca-9c6f-11ed-9682-7831c1bc31e4",
        value: 10,      // 10 -- положительная рецензия.
    }
)
// Получить родительские объекты вверх до корня у
// каждой реакции.
db.reactions.aggregate([
    {
        $graphLookup: {
            from: "reactions",
            startWith: "$target_id",
            connectFromField: "target_id",
            connectToField: "_id",
            as: "reactionsHierarchy"
        }
   }
])
// Посчитать средний рейтинг фильма на основе двух типов
// реакции: оценок и обзоров.  Упорядочить результат от
// большего среднего значения к меньшему.
db.reactions.aggregate([
    {
        $match: {
            "target_type": "movie",
            $or: [{type: "rating"}, {type: "review"},],
        }
    },
    {
        $group: {
            _id: "$target_id",
            avgReaction: { $avg : "$value" },
            totalReactions: { $count : { } }
        }
    },
    { $sort: { avgReactions: -1 } }
])
