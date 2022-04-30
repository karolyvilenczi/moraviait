
DB_USER = scraper_user
DB_PASS = scraper_pass
DB_NAME = scraper

# alembic init
alembic_init:
	docker-compose exec srv_fastapi alembic init -t async migrations

alembic_gen_first_migration:
	docker-compose exec srv_fastapi alembic revision --autogenerate -m "initial migration"

alembic_make_migration:
	docker-compose exec srv_fastapi alembic revision --autogenerate

alembic_migrate:
	docker-compose exec srv_fastapi alembic upgrade head

# --------------------------------------
# up


up_all:
	docker-compose up

reinit_migrations: up_all alembic_init
	

up_all_d:
	docker-compose up -d

stop_down:
	docker-compose stop
	docker-compose down

up_fastapi:
	docker-compose run srv_fastapi

up_fastapi_d:
	docker-compose -d run srv_fastapi


# --------------------------------------
# logs

logs:
	docker-compose logs -f

log_follow_fapi:
	docker-compose logs -f srv_fastapi

log_follow_mongo:
	docker-compose logs -f srv_mongodb

log_follow_postgres:
	docker-compose logs -f srv_postgres

# --------------------------------------
# build

build:
	docker-compose build --build-arg GROUP_ID=$$(id -g) --build-arg USER_ID=$$(id -u) --parallel

build_no_cache:
	docker-compose build --no-cache  --parallel    

rebuild_all: build up_all_d logs


# --------------------------------------
# enter
enter_mongo:
	docker exec -it cont_mongodb mongosh -u fapi_user -p fapi_pass --authenticationDatabase db_fapi

enter_postgres_bash:
	docker exec -it cont_postgres bash

enter_postgres_cli:
	docker exec -it cont_postgres psql -d $(DB_NAME) -U $(DB_USER)

enter_fapi:
	docker-compose run --rm  srv_fastapi bash

enter_fapi_ipython_postgres:
	docker-compose run --rm  srv_fastapi ipython -i ipython/create_orm_session.py 


# --------------------------------------
# utils

ps:
	docker ps --all

df:
	docker system df

create_net_dev:
	docker network create dev

# --------------------------------------
# prune, purge

prune_sys:
	docker system prune --all -f

prune_vol:
	docker volume prune  -f

prune_img:
	docker image prune --all -f

prune_net:
	docker network prune -f


docker purge: prune_sys prune_img prune_vol prune_net
