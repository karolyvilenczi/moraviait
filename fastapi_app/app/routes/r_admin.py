from fastapi import APIRouter

# ---------------------------------------------------------------

router = APIRouter(
    prefix = "/admin",
    tags = ["admin"],
    responses={404: {"description": "Not found"}},
)
# ---------------------------------------------------------------

# -----------------------------
@router.get("/ping")
async def get_pong():    
    return {
        "resp": "pong "    
        }


# ===============================================================
if __name__ == "__main__":
    msg = f"{__name__} started directly"
    print(msg)
else:
    msg = f"{__name__} loaded as a module"
    print(msg)
