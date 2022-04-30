
from pprint import pprint as pp

import sqlalchemy as sa

from app_models import app_db


# sync version
# class User(Base):
#     __tablename__ = "users"

#     id = sa.Column("id", sa.Integer, primary_key=True)
#     first_name = sa.Column(sa.String,)
#     last_name = sa.Column(sa.String,)
#     age = sa.Column(sa.Integer,)


# async version - current
users = sa.Table(
    "users",
    app_db.metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("first_name", sa.String),
    sa.Column("last_name", sa.String),
    sa.Column("age", sa.Integer)
)

# CRUD class for UsersModel

class UserCRUD:

    # -----------
    # get all users
    @classmethod
    async def get_all(cls, offset:int = 0, skip:int = 0):        

        resp = None                
        query = users.select()
        print(f"Getting all users using q: '{query}'")
        
        try:
            resp_users = await app_db.db.fetch_all(query)
        except Exception as e:
            print(f"Could not perform query {query}: {e}")
        else:
            resp = resp_users
        finally:
            return resp
    
    # -----------
    # get one user with ID
    @classmethod
    async def get_with_id(cls, id):        

        resp = None                
        q = users.select().filter(users.c.id == id)
        
        try:
            resp_user = await app_db.db.fetch_one(q)
        except Exception as e:
            print(f"CRUD: Could not execute query {q}: {e}")
            return None
        else:
            resp = resp_user
        finally:
            return resp

    # -----------
    # get one user with ID
    @classmethod
    async def delete_with_id(cls, id):        
        
        resp = None
        q = users.delete().where(users.c.id == id)
        try:
            resp_user_delete = await app_db.db.execute(q)
        except Exception as e:
            msg = f"CRUD: Could not delete user with id {id}, using q: {q}: {e}"
            print(msg)
            resp = msg        
        else:
            resp = "OK"
        
        return resp

    # -----------
    # create one user with **user data (dict)
    @classmethod
    async def create(cls, **user):
        resp = None
        
        query = users.insert().values(**user)
        
        try:
            resp_user_id = await app_db.db.execute(query)
        except Exception as e:
            print(f"Could not perform query {query}: {e}")
        else:
            resp = resp_user_id
        finally:
            return resp


    # -----------
    # create one user with **user data (dict)
    @classmethod
    async def update(cls, **user_data):
        resp = None
        
        # get the id out from the dict
        id_to_update = user_data.get('id')
        user_data.pop('id')

        # print(id_to_find)
        # print(user_data)

        # this works by finding the user by the id, and updates it with the rest (in the JSON body)
        query_update = users.update().where(
            users.c.id == id_to_update
        ).values(**user_data)

        try:
            resp_user_id = await app_db.db.execute(query_update)
        except Exception as e:
            print(f"Could not perform query {query_update}: {e}")
        finally:
            # get the updated row
            updated_row = await UserCRUD.get_with_id(id = id_to_update)
            return updated_row

