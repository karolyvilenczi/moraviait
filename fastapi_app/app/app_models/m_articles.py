
from pprint import pprint as pp

import sqlalchemy as sa

from itertools import chain

from app_models import app_db


# async version - current
articles = sa.Table(
    "articles",
    app_db.metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("url", sa.String),
    sa.Column("text", sa.String),    
)

# CRUD class for UsersModel

class ArticleCRUD:

    # -----------
    # get all articles
    @classmethod
    async def get_all(cls, offset:int = 0, skip:int = 0):        

        resp = None                
        query = articles.select()
        print(f"Getting all articles using q: '{query}'")
        
        try:
            resp_articles = await app_db.db.fetch_all(query)
        except Exception as e:
            print(f"Could not perform query {query}: {e}")
        else:
            resp = resp_articles
        finally:
            return resp
    
    # -----------
    # get one user with ID
    @classmethod
    async def get_with_id(cls, id):        

        resp = None                
        q = articles.select().filter(articles.c.id == id)
        
        try:
            resp_article = await app_db.db.fetch_one(q)
        except Exception as e:
            print(f"CRUD: Could not execute query {q}: {e}")
            return None
        else:
            resp = resp_article
        finally:
            return resp

    # -----------
    # get one user with ID
    @classmethod
    async def delete_with_id(cls, id):        
        
        resp = None
        q = articles.delete().where(articles.c.id == id)
        try:
            resp_article_delete = await app_db.db.execute(q)
        except Exception as e:
            msg = f"CRUD: Could not delete article with id {id}, using q: {q}: {e}"
            print(msg)
            resp = msg        
        else:
            resp = "OK"
        
        return resp

    # -----------
    # create one article with **article data (dict)
    @classmethod
    async def create(cls, **article):
        resp = None
        
        query = articles.insert().values(**article)
        
        try:
            resp_article_id = await app_db.db.execute(query)
        except Exception as e:
            print(f"Could not perform query {query}: {e}")
        else:
            resp = resp_article_id
        finally:
            return resp


    # -----------
    # create one user with **user data (dict)
    @classmethod
    async def update(cls, **article_data):
        resp = None
        
        # get the id out from the dict
        id_to_update = article_data.get('id')
        article_data.pop('id')

        # this works by finding the article by the id, and updates it with the rest (in the JSON body)
        query_update = articles.update().where(
            articles.c.id == id_to_update
        ).values(**article_data)

        try:
            resp_article_id = await app_db.db.execute(query_update)
        except Exception as e:
            print(f"Could not perform query {query_update}: {e}")
        finally:
            # get the updated row
            updated_row = await ArticleCRUD.get_with_id(id = id_to_update)
            return updated_row


    # -----------
    # get all articles with a keyword in them
    @classmethod
    async def get_all_based_on_keywords(cls, keywords:list = [], offset:int = 0, skip:int = 0):        

        resp_list = list()
        query_list = [
            articles.select().with_only_columns([articles.c.text, articles.c.url ]).where(articles.c.text.like(f"%{keyword}%")) for keyword in keywords
        ]
       
        print(f"Getting all articles containing keywords '{keywords}' using queries: '{query_list}'")
        
        for q in query_list:
            resp = None
            try:
                resp_articles = await app_db.db.fetch_all(q)
            except Exception as e:
                print(f"Could not perform query {q}: {e}")
            else:
                resp = resp_articles
            finally:
                if resp is not None:
                    resp_list.append(resp)
            
            # flatten the resp_list
            resp_one_list = list(chain(*resp_list))
            # print(resp_one_list)
        
        return resp_one_list