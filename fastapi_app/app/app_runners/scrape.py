import json
from re import U
from sre_parse import parse_template
import requests

from bs4 import BeautifulSoup
import soupsieve as sv
from yaml import parse

# from lxml import etree

from app_models import m_articles

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

    content = await get_page_content(url = url)
    results_headline_list = await parse_content(content=content, css_selector_logic = selector_logic)


    for headline in results_headline_list:
        art_dict = {
            "url": url, 
            "text": headline
        }

        article_id = await m_articles.ArticleCRUD.create(**art_dict)

    resp = {
        f"number of articles inserted for {url}": len(results_headline_list)
    }
    # print(article_id)
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
