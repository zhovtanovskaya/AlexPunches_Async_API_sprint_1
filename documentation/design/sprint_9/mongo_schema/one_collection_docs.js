// Примеры документов реакций пользователей на контент
// для одной коллекции "reactions".

// Рейтинг фильма.
db.reactions.insertOne({
    // _id
    created_at: new Date(),
    user_id: "60bf29d4-9c6f-11ed-a1a5-7831c1bc31e4",          // UUID.
    target_id: "6fdcc8ca-9c6f-11ed-9682-7831c1bc31e4",        // Movie UUID.
    target_type: "movie",
    type: "rating",
    value: 5    // [0..10]
})
// Обзор на фильм.
db.reactions.insertOne({
    created_at: new Date(),
    user_id: "60bf29d4-9c6f-11ed-a1a5-7831c1bc31e4",          // UUID.
    target_id: "6fdcc8ca-9c6f-11ed-9682-7831c1bc31e4",        // Movie UUID.
    target_type: "movie",
    type: "review",
    value: 5, // [0, 5, 10]
    title: "So-so movie.",
    text: "Long and detailed explanations..."
})
// Лайк на обзор.
db.reactions.insertOne({
    // _id
    created_at: new Date(),
    user_id: "af18023d-9c76-11ed-9485-7831c1bc31e4",          // UUID.
    target_id: ObjectId("63d0c92bf5eb85d9a10bd8ac"),          // Review UUID.
    target_type: "review",
    type: "like",
    value: 10, // [0, 10]
})
