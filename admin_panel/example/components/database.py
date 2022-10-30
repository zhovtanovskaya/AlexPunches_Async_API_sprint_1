import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB_ADMIN'),
        'USER': os.environ.get('POSTGRES_USER_ADMIN'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD_ADMIN'),
        'HOST': os.environ.get('DB_HOST_ADMIN', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT_ADMIN', 5432),
        'OPTIONS': {
           'options': '-c search_path=public,content'
        }
    }
}