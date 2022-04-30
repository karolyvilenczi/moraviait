from app_models.m_articles import ArticleCRUD

async def run_scraper():
    resp = await ArticleCRUD.get_all()
    print(f">>>>>>>>> {resp}")
    return resp


# ===============================================================
if __name__ == "__main__":
    msg = f"{__name__} started directly"    
    print(msg)
    # print(sys.path)
else:
    msg = f"{__name__} started as a module."
    print(msg)
    # print(sys.path)
