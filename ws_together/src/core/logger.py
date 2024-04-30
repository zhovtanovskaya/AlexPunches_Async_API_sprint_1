LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DEFAULT_HANDLERS = ['console', 'file']
LOG_FILE = '/var/log/ws_together/ws_together.log'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': LOG_FORMAT
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': """
                asctime: %(asctime)s
                created: %(created)f
                filename: %(filename)s
                funcName: %(funcName)s
                levelname: %(levelname)s
                levelno: %(levelno)s
                lineno: %(lineno)d
                message: %(message)s
                module: %(module)s
                msec: %(msecs)d
                name: %(name)s
                pathname: %(pathname)s
                process: %(process)d
                processName: %(processName)s
                relativeCreated: %(relativeCreated)d
                thread: %(thread)d
                threadName: %(threadName)s
                exc_info: %(exc_info)s
            """,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'formatter': 'json',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE,
        },
    },
    'loggers': {
        '': {
            'handlers': LOG_DEFAULT_HANDLERS,
            'level': 'INFO',
        },
    },
    'root': {
        'level': 'INFO',
        'formatter': 'verbose',
        'handlers': LOG_DEFAULT_HANDLERS,
    },
}
