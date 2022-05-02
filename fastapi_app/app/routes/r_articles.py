
from ast import keyword
from webbrowser import get
from pydantic import (
    ValidationError
)

from fastapi import (
    APIRouter,
    HTTPException, 
    status,
    Path,
    Query,
    Body, 
    Header,
)

from app_models import m_articles
import app_schema

# ---------------------------------------------------------------
router = APIRouter(
    prefix = "/article",
    tags = ["articles"],
    responses={404: {"description": "Not found"}},
)

# ---------------------------------------------------------------

# -----------------------------
# select all
@router.get("/", response_model = app_schema.AllArticlesSchema)
async def fetch_all_articles():    
    article_list = []
    
    # 1. Is the data (returned from the DB ) NOT None?
    try:
        article_objects = await m_articles.ArticleCRUD.get_all()        
    except Exception as e:
        msg = f"Could not get articles from db: {e}"
        # TODO: replace w. logger
        print(msg)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = msg)
    
    # 2. Can it be unpacked and validated?
    try:
        article_list = [
            app_schema.ArticleSchema(**article) for article in article_objects
        ]               
    except ValidationError as ve:
        # TODO: replace w. logger
        print(f"Validation error:")
        print(f"{ve.json()}")
        return None
    except Exception as e:
        # TODO: replace w. logger
        print(f"Other error:")
        print(f"{e}")
        return None
    
    # 3. If all OK, return into the schema
    return {"articles": article_list}

# -----------------------------
# select one w. id
@router.get("/{id}", response_model = app_schema.ArticleSchema)
async def fetch_article(id:int = 0):
    
    article_found = None    
    
    resp_obj = await m_articles.ArticleCRUD.get_with_id(id)

    # 1. Is the data (returned from the DB ) NOT None?
    if resp_obj is None:
        msg = f"Articles found: {resp_obj}."
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = msg)

    # 2. Can it be unpacked and validated?
    try:
        article_found = app_schema.ArticleSchema(**resp_obj)
    except ValidationError as ve:
        # TODO: replace w. logger
        print(f"Validation error:")
        print(f"{ve.json()}")
        return resp_obj
    except Exception as e:
        # TODO: replace w. logger
        print(f"Other error:")
        print(f"{e}")
        return resp_obj
    
    # 3. If all OK, return the article found
    return article_found

# -----------------------------
# insert one
@router.post("/")
async def create_article(article:app_schema.ArticleSchema):
    try:
        article_id = await m_articles.ArticleCRUD.create(**article.dict())
    except Exception as e:
        msg = f"Could not create article from obj {article}: {e}"
        # TODO: replace w. logger
        print(msg)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = msg)
    else:
        return {
            "created_article_id": article_id
            }


# -----------------------------
# search for articles based on keywords
@router.post("/find")
async def search_for_kw_in_articles(payload:app_schema.KeywordSchema):
    
    try:
        article_objects_found = await m_articles.ArticleCRUD.get_all_based_on_keywords(**payload.dict())        

    except Exception as e:
        msg = f"Could not find any article from keywords {payload}: {e}"
        # TODO: replace w. logger
        print(msg)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = msg)
    else:
        return {
            "articles": article_objects_found
            }


# -----------------------------
# update one w. id
@router.put("/")
async def update_article(article:app_schema.UpdateArticleSchema):
    try:
        updated_article = await m_articles.ArticleCRUD.update(**article.dict())
    except Exception as e:
        msg = f"Could not update article from obj {article}: {e}"
        print(msg)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = msg)
    
    return {
        "updated": updated_article
    }


# -----------------------------
# delete one w. id
@router.delete("/{id}")
async def delete_article(id:int = 0):
    
    try:
        article_deleted = await m_articles.ArticleCRUD.delete_with_id(id = id)
    except Exception as e:
        msg = f"Could not find article with id {id}: {e}"
        # TODO: replace w. logger
        print(msg)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = msg)

    return {"article_deleted": article_deleted}        
           
        



# ===============================================================
if __name__ == "__main__":
    msg = f"{__name__} started directly"
    print(msg)
else:
    msg = f"{__name__} loaded as a module"
    print(msg)
