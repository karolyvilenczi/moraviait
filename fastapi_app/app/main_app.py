
# system imports
import os
# import sys

from typing import (
    Tuple, 
    List, 
    Optional
)

# imports for FastAPI and related
from fastapi import (
    FastAPI, 
    Depends, 
    Header,
    Query, 
    Path, 
    Body,
    HTTPException, 
    status
)

# for the repeated tasks- while the server is running
from fastapi_utils.tasks import (
    repeat_every
)

# to handle DB management w. the databases libr
import sqlalchemy as sa

# ---------------------------------------------------------------
# import db management module
from app_models import (
    app_db
)

# import scraping module
from app_runners import (
    scrape
)

# ---------------------------------------------------------------
# import routes
from routes import (
    r_admin, 
    r_users, 
    r_articles
)

# ---------------------------------------------------------------
# init api token
#API_TOKEN = "SECRET API TOKEN"
SECRET_HEADER = "SECRET_VAL" # this has to be sent over as SECRET-HEADER -> SECRET_VAL
SCRAPING_FREQ = int(os.environ.get('SCRAPING_FREQUENCY_SECONDS'))

# ---------------------------------------------------------------
# dependencies

# ---------------------------------------------------------------
# make fapi obj
ep_obj = FastAPI()
ep_obj.include_router(r_users.router)
ep_obj.include_router(r_articles.router)
ep_obj.include_router(r_admin.router)

# ---------------------------------------------------------------
# startup and shutdown events
# -----------------------------
@ep_obj.on_event("startup")
async def startup():    
    print(f"----> Starting up:")
    print(f"----> Scraping frequency is set to {SCRAPING_FREQ} seconds.")
    print(f"----> Calling DB connect()...")    
    await app_db.db.connect()

# -----------------------------
@ep_obj.on_event("startup")
@repeat_every(seconds=SCRAPING_FREQ) 
async def run_scraper() -> None:    
    url = "https://www.idnes.cz/"
    css_logic = "h3:is(.art h3)"

    scrape_res = await scrape.run_scraper_for( 
        url = url, selector_logic = css_logic
    )
    
    print(f"SCRAPER STAT: {scrape_res}")

# -----------------------------
@ep_obj.on_event("startup")
@repeat_every(seconds=SCRAPING_FREQ) 
async def run_scraper() -> None:    
    url = "https://www.bbc.com/"
    css_logic = "a:is(.media__link)"

    scrape_res = await scrape.run_scraper_for( 
        url = url, selector_logic = css_logic
    )
    
    print(f"SCRAPER STAT: {scrape_res}")

# -----------------------------
@ep_obj.on_event("shutdown")
async def startup():    
    print(f"----> Shutting down up:")
    print(f"----> Calling DB disconnect()...")    
    await app_db.db.disconnect()



# ===============================================================
if __name__ == "__main__":
    msg = "MAIN APP started directly"    
    print(msg)
    # print(sys.path)
else:
    msg = "MAIN APP started as a module."
    print(msg)
    # print(sys.path)
