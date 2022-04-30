from curses import meta
import os
import databases
import sqlalchemy as sa

APP_DB_USER=os.environ.get('APP_DB_USER')
APP_DB_PASS=os.environ.get('APP_DB_PASS')
APP_DB_NAME=os.environ.get('APP_DB_NAME')
DATABASE_SERVICE_NAME=os.environ.get('DATABASE_SERVICE_NAME')

DATABASE_URL_ASYNC=f"postgresql+asyncpg://{APP_DB_USER}:{APP_DB_PASS}@{DATABASE_SERVICE_NAME}:5432/{APP_DB_NAME}"

# used to play with sa from ipython
DATABASE_URL=f"postgresql+psycopg2://{APP_DB_USER}:{APP_DB_PASS}@{DATABASE_SERVICE_NAME}:5432/{APP_DB_NAME}"

print(f"{__name__}: Using DB Conn str: {DATABASE_URL_ASYNC=}")

db = databases.Database(DATABASE_URL_ASYNC)
metadata = sa.MetaData()
