"""Точка входа в приложение."""

from config import settings


def main() -> None:
    """Запустить загрузку, предварительно уточнить начальные данные."""
    print('Куда загружать будем?\n'
          'c) Clickhouse\n'
          'a) Async Clickhouse for 3 shards\n'
          'v) Vertica\n'
          'm) Mongo',
          )
    cloud = str(input('c/a/v/m>'))

    print('Сколько юзеров?')
    users_count = int(input(f'default {settings.fake_users_count}>')
                      or settings.fake_users_count)

    print('Сколько фильмов?')
    films_count = int(input(f'default {settings.fake_films_count}>')
                      or settings.fake_users_count)

    print('Какой chunk_size?')
    chunk_size = int(input(f'default {settings.chunk_size}>')
                     or settings.chunk_size)

    if cloud == 'c':
        import clickhouse.clear_data as clear_ch
        import clickhouse.load_fake_data as sync_ch
        clear_ch.run()
        sync_ch.run(users_count, films_count, chunk_size)
    elif cloud == 'a':
        import asyncio

        import clickhouse.async_load_fake_data_2 as async_ch
        import clickhouse.clear_data as clear_ch
        clear_ch.run()
        asyncio.run(async_ch.run(users_count, films_count, chunk_size))
    elif cloud == 'v':
        from vertica import load_vertica
        load_vertica.run(users_count, films_count, chunk_size)
    elif cloud == 'm':
        from mongo import load_mongo
        load_mongo.run(users_count, films_count, chunk_size)
    else:
        print('\n\nВсе таки...')
        main()


if __name__ == '__main__':
    main()
