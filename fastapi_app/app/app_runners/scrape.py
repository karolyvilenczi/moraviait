import requests

from bs4 import BeautifulSoup
import soupsieve as sv

from app_models import m_articles

# ---------------------------------------------------------------

async def get_page_content(url = ""):

    try:
    
        response = requests.get(url)
    
    except ConnectionError as ce:
        print(f"Could not open url {url}: {ce}")
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
async def run_scraper_for(url:str = None, selector_logic:str = None, insert_to_db:bool = True):

    content = await get_page_content(url = url)
    results_headline_list = await parse_content(content=content, css_selector_logic = selector_logic)


    for headline in results_headline_list:
        art_dict = {
            "url": url, 
            "text": headline
        }

        if insert_to_db:
            article_id = await m_articles.ArticleCRUD.create(**art_dict)
        else:
            print("Will not insert into DB.")

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
