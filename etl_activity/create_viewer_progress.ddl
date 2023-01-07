-- Создать Kafka Table Engine для загрузки событий о прогрессе
-- просмотра фильма.  Ожидается, что ключ события это строка вида
-- "user_uuid+film_uuid".  Значение события это JSON '{"time": seconds}'.
--
-- ВНИМАНИЕ: В строке `SETTINGS kafka_broker_list` должен быть
--           указан CSV-список брокеров Kafka в формате host:port.
CREATE TABLE viewer_progress_queue (
    time UInt32
) ENGINE = Kafka
SETTINGS kafka_broker_list = 'enter_kafka_host:9092',
         kafka_topic_list = 'viewer_progress',
         kafka_group_name = 'clickhouse',
         kafka_format = 'JSONEachRow';


-- Создать таблицу для сохранения прогресса просмотра фильма.
CREATE TABLE viewer_progress
(
    user_id UUID,
    film_id UUID,
    film_frame_time UInt32,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY user_id;


-- Создать materialized view, которая выделяет UUID пользователя
-- и UUID фильма из ключа Kafka-события.  И создает запись для этого
-- события в таблице viewer_progress.
CREATE MATERIALIZED VIEW viewer_progress_materialized_view TO viewer_progress
    AS SELECT
        splitByChar('+', _key)[1] as user_id,
        splitByChar('+', _key)[2] as film_id,
        time as film_frame_time
    FROM viewer_progress_queue;
