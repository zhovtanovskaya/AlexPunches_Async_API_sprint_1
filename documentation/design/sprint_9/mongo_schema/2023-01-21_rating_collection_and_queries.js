// Возможная схема коллекции с рейтингами.
// Версия от 2023-01-21.
db.ratings.insertOne({
    // _id
    movie_id: 1,
    user_id: 3,
    rating: 5,
    created_at: new Date(),
})

db.ratings.updateOne(
  {_id: ObjectId("63cbcafaf07c838bc58f9a0d"),},
  {$set: {rating: 3},},
)

db.ratings.deleteOne({ _id: ObjectId("63cbcafaf07c838bc58f9a0d")})

db.ratings.aggregate([
    { $match: {"movie_id": 1} },
    { $group: {_id: "$movie_id", totalRatings: { $count : { } } } },
    { $sort: { totalRatings: -1 } }
])

db.ratings.aggregate([
    {
        $group: {
            _id: "$movie_id", avgRatings: { $avg : "$rating" }, totalRatings: { $count : { } }
        }
    },
    { $sort: { avgRatings: -1 } }
])

db.ratings.aggregate([
    {$sort: {_id: -1}},
    {$skip: 1},
    {$limit: 2},
])
db.ratings.find().count()
db.ratings.find().limit(3).skip(1)

db.ratings.aggregate(
  [
    {
      $match: {rating: { $gt: 5 } }
    },
    {
      $count: "passing_ratings"
    }
  ]
)
