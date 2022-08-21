film_work_2_es = """SELECT
    fw.id,
    fw.title,
    fw.description,
    fw.rating,
    fw.type,
    fw.creation_date as created,
    fw.updated_at as modified,
    array_agg(DISTINCT g.name) as genre,
    array_agg(DISTINCT p.full_name) FILTER(
        WHERE p.id is not null AND pfw.role = 'actor'
    ) as actors_names,
    array_agg(DISTINCT p.full_name) FILTER(
        WHERE p.id is not null AND pfw.role = 'writer'
    ) as writers_names,

    COALESCE (
            json_agg(DISTINCT p.full_name) FILTER(
                WHERE p.id is not null AND pfw.role = 'director'
                ),
            '[]'
        ) as director,
    COALESCE (
            json_agg(
                DISTINCT jsonb_build_object(
                    'id', p.id,
                    'name', p.full_name
                )
            ) FILTER (WHERE p.id is not null AND pfw.role = 'director'),
            '[]'
        ) as directors,
    COALESCE (
            json_agg(
                DISTINCT jsonb_build_object(
                    'id', p.id,
                    'name', p.full_name
                )
            ) FILTER (WHERE p.id is not null AND pfw.role = 'actor'),
            '[]'
        ) as actors,
    COALESCE (
            json_agg(
                DISTINCT jsonb_build_object(
                    'id', p.id,
                    'name', p.full_name
                )
            ) FILTER (WHERE p.id is not null AND pfw.role = 'writer'),
            '[]'
        ) as writers,
    COALESCE (
        json_agg(
            DISTINCT jsonb_build_object(
                'id', g.id,
                'name', g.name
            )
        ) FILTER (WHERE g.id is not null),
        '[]'
    ) as genres

FROM content.film_work fw
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
WHERE
    fw.updated_at > %(timestamp)s
    OR
    g.updated_at > %(timestamp)s
    OR
    p.updated_at > %(timestamp)s
GROUP BY fw.id
;
"""

genre_2_es = """SELECT
    g.id, g.name, g.description
FROM content.genre g
WHERE
    g.updated_at > %(timestamp)s
ORDER BY g.id
;
"""

person_2_es = """SELECT
    p.id, p.full_name as name
FROM content.person p
WHERE
    p.updated_at > %(timestamp)s
ORDER BY p.id
;
"""
