
# system imports
import os
# import sys


from typing import (
    Tuple, 
    List, 
    Optional
)


# 3rd party imports
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

# to handle DB management w. the databases libr
import sqlalchemy as sa


# ---------------------------------------------------------------
# import db management module

from app_models import app_db

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

@ep_obj.on_event("startup")
async def startup():    
    print(f"----> Starting up:")
    print(f"----> Calling DB connect()...")    
    await app_db.db.connect()
    


@ep_obj.on_event("shutdown")
async def startup():    
    print(f"----> Shutting down up:")
    print(f"----> Calling DB disconnect()...")    
    await app_db.db.disconnect()



# ===============================================================
if __name__ == "__main__":
    msg = "App started directly"    
    print(msg)
    # print(sys.path)
else:
    msg = "App started as a module."
    print(msg)
    # print(sys.path)
