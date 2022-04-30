from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


print(f"Importing DATABASE_URL")
from app_models.app_db import DATABASE_URL

print(f"Importing models")
from app_models.m_users import users

# ----------------------------------------------------------
print(f"DB conn str: {DATABASE_URL}")

# -----------------------------
pg_engine = create_engine(DATABASE_URL)
print(f"PG Engine obj: {pg_engine}")

# -----------------------------
Session = sessionmaker(bind=pg_engine)
pg_sess = Session()
print(f"PG Session obj: {pg_sess}")

# -----------------------------
sample_q = pg_sess.query(users).first()
print(f"Sample q: 'pg_sess.query(users).first()': {sample_q}")



