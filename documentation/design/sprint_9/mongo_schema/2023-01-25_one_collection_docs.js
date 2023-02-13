// Примеры документов реакций пользователей на контент
// для одной коллекции "reactions".
// Версия от 2023-01-25.
db.reactions.insertOne({
    // _id
    created_at: new Date(),
    user_id: "60bf29d4-9c6f-11ed-a1a5-7831c1bc31e4",          // UUID.
    target_id: "6fdcc8ca-9c6f-11ed-9682-7831c1bc31e4",        // Movie UUID.
    target_type: "movie",
    type: "rating",
    value: 5    // [0..10]
    // value: 'neutral',
})
db.reactions.insertOne({
    // _id
    created_at: new Date(),
    user_id: "60bf29d4-9c6f-11ed-a1a5-7831c1bc31e4",          // UUID.
    target_id: "6fdcc8ca-9c6f-11ed-9800-7831c1bc31e4",        // Movie UUID.
    target_type: "movie",
    type: "rating",
    value: 8    // [0..10]
    // value: 'neutral',
})
// Обзор на фильм.
db.reactions.insertOne({
    _id: ObjectId("63d0c92bf5eb85d9a10bd8ac"),
    created_at: new Date(),
    user_id: "60bf29d4-9c6f-11ed-a1a5-7831c1bc31e4",          // UUID.
    target_id: "6fdcc8ca-9c6f-11ed-9682-7831c1bc31e4",        // Movie UUID.
    target_type: "movie",
    type: "review",
    value: 5, // [0 - отрицательная, 5 - нейтральная, 10 - положительная]
    // value: 'thumb_up'
    title: "So-so movie.",
    text: "Long and detailed explanations..."
})
db.reactions.insertOne({
    _id: ObjectId("63d2651655dfa9351270284b"),
    created_at: new Date(),
    user_id: "60bf29d4-9c6f-11ed-9400-7831c1bc31e4",          // UUID.
    target_id: "6fdcc8ca-9c6f-11ed-9682-7831c1bc31e4",        // Movie UUID.
    target_type: "movie",
    type: "review",
    value: 10, // [0 - отрицательная, 5 - нейтральная, 10 - положительная]
    // value: 'thumb_up'
    title: "Must see!",
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
db.reactions.insertOne({
    // _id
    created_at: new Date(),
    user_id: "af18023d-9c76-11ed-9400-7831c1bc31e4",          // UUID.
    target_id: ObjectId("63d0c92bf5eb85d9a10bd8ac"),          // Review UUID.
    target_type: "review",
    type: "like",
    value: 10, // [0, 10]
})
db.reactions.insertOne({
    // _id
    created_at: new Date(),
    user_id: "60bf29d4-9c6f-11ed-a1a5-7831c1bc31e4",          // UUID.
    target_id: ObjectId("63d0c92bf5eb85d9a10bd8ac"),          // Review UUID.
    target_type: "review",
    type: "like",
    value: 0, // [0, 10]
})
db.reactions.insertOne({
    // _id
    created_at: new Date(),
    user_id: "60bf29d4-9c6f-11ed-a1a5-7831c1bc31e4",          // UUID.
    target_id: ObjectId("63d2651655dfa9351270284b"),          // Review UUID.
    target_type: "review",
    type: "like",
    value: 0, // [0, 10]
})