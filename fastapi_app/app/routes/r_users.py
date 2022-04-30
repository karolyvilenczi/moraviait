
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

from app_models import m_users
import app_schema

# ---------------------------------------------------------------
router = APIRouter(
    prefix = "/user",
    tags = ["users"],
    responses={404: {"description": "Not found"}},
)

# ---------------------------------------------------------------

# -----------------------------
# select all
@router.get("/", response_model = app_schema.AllUsersSchema)
async def fetch_all_users():    
    user_list = []
    
    # 1. Is the data (returned from the DB ) NOT None?
    try:
        user_objects = await m_users.UserCRUD.get_all()        
    except Exception as e:
        msg = f"Could not get users from db: {e}"
        print(msg)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = msg)
    
    # 2. Can it be unpacked and validated?
    try:
        user_list = [
            app_schema.UserSchema(**user) for user in user_objects
        ]               
    except ValidationError as ve:
        print(f"Validation error:")
        print(f"{ve.json()}")
        return None
    except Exception as e:
        print(f"Other error:")
        print(f"{e}")
        return None
    
    # 3. If all OK, return into the schema
    return {"users": user_list}

# -----------------------------
# select one w. id
@router.get("/{id}", response_model = app_schema.UserSchema)
async def fetch_users(id:int = 0):
    
    user_found = None    
    
    resp_obj = await m_users.UserCRUD.get_with_id(id)

    # 1. Is the data (returned from the DB ) NOT None?
    if resp_obj is None:
        msg = f"Users found: {resp_obj}."
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = msg)

    # 2. Can it be unpacked and validated?
    try:
        user_found = app_schema.UserSchema(**resp_obj)
    except ValidationError as ve:
        print(f"Validation error:")
        print(f"{ve.json()}")
        return resp_obj
    except Exception as e:
        print(f"Other error:")
        print(f"{e}")
        return resp_obj
    
    # 3. If all OK, return the user found
    return user_found


# -----------------------------
# insert one
@router.post("/")
async def create_users(user:app_schema.UserSchema):
    try:
        user_id = await m_users.UserCRUD.create(**user.dict())
    except Exception as e:
        msg = f"Could not create user from obj {user}: {e}"
        print(msg)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = msg)
    else:
        return {
            "created_user_id": user_id
            }


# -----------------------------
# update one w. id
@router.put("/")
async def update_user(user:app_schema.UpdateUserSchema):
    try:
        updated_user = await m_users.UserCRUD.update(**user.dict())
    except Exception as e:
        msg = f"Could not update user from obj {user}: {e}"
        print(msg)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = msg)
    
    return {
        "updated": updated_user
    }


# -----------------------------
# delete one w. id
@router.delete("/{id}")
async def delete_user(id:int = 0):
    
    try:
        user_deleted = await m_users.UserCRUD.delete_with_id(id = id)
    except Exception as e:
        msg = f"Could not find user with id {id}: {e}"
        print(msg)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = msg)

    return {"user_deleted": user_deleted}        

        
        
        



# ===============================================================
if __name__ == "__main__":
    msg = f"{__name__} started directly"
    print(msg)
else:
    msg = f"{__name__} loaded as a module"
    print(msg)
