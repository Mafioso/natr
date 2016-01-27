from .dev import *

# print os.getenv('POSTGRES_PORT_5432_TCP_PORT')
# for k in os.environ:
#     if k.startswith('DB_'):
#         print k, os.environ[k]
    # if k.startswith('DB_ENV'):
    #     print k
    

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.getenv('DB_ENV_POSTGRES_DB', 'natr_dev'),                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': os.getenv('DB_ENV_POSTGRES_USER', 'mars'),
        'PASSWORD': os.getenv('DB_ENV_POSTGRES_PASSWORD', '2050'),
        'HOST': os.getenv('DB_PORT_5432_TCP_ADDR', 'localhost'),                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
        'PORT': os.getenv('DB_PORT_5432_TCP_PORT', 5432),                      # Set to empty string for default.
    }
}
