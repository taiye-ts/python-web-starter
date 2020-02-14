from os import environ

DB_USER = environ['DB_USER']
DB_PASSWORD = environ['DB_PASSWORD']
DB_DB = environ['DB_DB']
DATABASE_HOST = environ['DB_HOST']
DB_PORT = environ['DB_PORT']
ALCHEMY_DRIVER = environ['ALCHEMY_DRIVER']
DATABASE_URL = '{}://{}:{}@{}:{}/{}'.format(
    ALCHEMY_DRIVER, DB_USER, DB_PASSWORD, DB_DB, DATABASE_HOST, DB_PORT,
)
