# TO start up in a new env.:

1. run 'make build'
2. run' docker network create dev'
3. run 'make up_all' or 'make up_all_d'

4. To do DB migrations w. Alembic:
4.1. run 'make alembic_init'

In the generated migrations folder configure:
- in env.py:

import app_models

from app_models import app_db
target_metadata = app_db.metadata

- in alebic.ini:
add: 'sqlalchemy.url=postgresql+asyncpg://scraper_user:scraper_pass@srv_postgres:5432/scraper'

4.2. run 'make alembic_gen_first_migration'
( observe the migrations generated in the 'migrations' folder: should contain the SA fields picked up from the app_models)

4.3. run 'make alembic_migrate'


