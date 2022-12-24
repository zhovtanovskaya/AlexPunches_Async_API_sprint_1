CREATE TABLE film_frame
(
    user_id UUID,
    movie_id UUID,
    time UInt32,
    created_at DateTime
) ENGINE = MergeTree()
ORDER BY user_id;
