"""Скрипт можно запустить и наблюдать как данные добавляются в Вертику."""
import csv
from dataclasses import dataclass
from time import sleep

import vertica_python
from config import logger, settings
from vertica_python import Connection


@dataclass
class ActualData:
    """Класс количества данных из Вертики."""

    all_data_count: int


def get_data(connection: Connection) -> ActualData:
    """Получить информацию о количестве данных в Вертике."""
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM views')
    count = cursor.fetchone()[0]
    return ActualData(all_data_count=count)


def main():
    """Получить данные из Вертики и вывести в лог."""
    connect = vertica_python.connect(**settings.vertica_connection_info)
    last_all_data = 0
    log_file = open('./lods.csv', 'a', newline='')
    writer = csv.writer(log_file)
    try:
        while last_all_data < settings.cheker_count:
            actual_data = get_data(connect)
            how_much_added = actual_data.all_data_count - last_all_data
            last_all_data = actual_data.all_data_count
            writer.writerow([actual_data.all_data_count, f'+{how_much_added}'])
            logger.info(f'{actual_data.all_data_count:_} +{how_much_added:_}')

            sleep(settings.cheker_interval)
    except KeyboardInterrupt:
        logger.info('exit')
    finally:
        connect.close()
        log_file.close()


if __name__ == '__main__':
    main()
