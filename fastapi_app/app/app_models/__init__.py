# for the command 'alembic revision --autogenerate -m "initial migration"' to pick up the models 
# I am importing the relevant ones HeaderRegistry
# and in in 'emv.py' all I needed was to import 
# 'import app_models' instead
# 'from app_models import m_users'

from . import m_users