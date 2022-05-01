import json
from re import U
from sre_parse import parse_template
import requests

from bs4 import BeautifulSoup
import soupsieve as sv
from yaml import parse

# from lxml import etree

from app_models.m_articles import ArticleCRUD

# ---------------------------------------------------------------

async def get_page_content(url = ""):
    try:
        response = requests.get(url)
    except Exception as e:
        print(f"Could not load {url}: {e}")
        return None
    else:
        if response.status_code != 200:
            print("Error fetching page")
            return None
        else:
            content = response.content
            return content

async def parse_content(content:str = None, css_selector_logic:str = None):
    soup = BeautifulSoup(content, 'html5lib')
    # e.g. selector for idnes: 'h3:is(.art h3)'

    return [elem.text.strip() for elem in sv.select(css_selector_logic,soup)]


# ---------------------------------------------------------------
async def run_scraper_for(url:str = None, selector_logic:str = None):
    # resp = await ArticleCRUD.get_all()

    # URL = "https://www.idnes.cz/"
    # SELECTOR_LOGIC = 'h3:is(.art h3)'

    content = await get_page_content(url = url)
    results = await parse_content(content=content, css_selector_logic = selector_logic)

    # print(results)
    return results

    
    


# ===============================================================
if __name__ == "__main__":
    msg = f"{__name__} started directly"    
    print(msg)

    # print(sys.path)
else:
    msg = f"{__name__} started as a module."
    print(msg)
    # print(sys.path)
