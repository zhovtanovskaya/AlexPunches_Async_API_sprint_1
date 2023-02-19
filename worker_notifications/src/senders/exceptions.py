"""Кастомные исключения для сендеров."""


class DeadlineNotifyError(Exception):
    pass


class TimeOfDayNotifyError(Exception):
    pass
