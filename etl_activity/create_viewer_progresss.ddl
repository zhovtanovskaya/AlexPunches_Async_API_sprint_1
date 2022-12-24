CREATE TABLE viewer_progress_queue (
    time UInt32
) ENGINE = Kafka
SETTINGS kafka_broker_list = '158.160.23.155:9092',
         kafka_topic_list = 'viewer_progress',
         kafka_group_name = 'clickhouse',
         kafka_format = 'JSONEachRow';


CREATE TABLE viewer_progress
(
    user_id UUID,
    film_id UUID,
    film_frame_time UInt32,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY user_id;


CREATE MATERIALIZED VIEW d TO viewer_progress
    AS SELECT
        splitByChar('+', _key)[1] as user_id,
        splitByChar('+', _key)[2] as film_id,
        time as film_frame_time
    FROM viewer_progress_queue;
