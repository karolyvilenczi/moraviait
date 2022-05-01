
import requests
from bs4 import BeautifulSoup
import soupsieve as sv


def get_page_content(url = ""):
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


def parse_content(content:str = None, css_selector_logic:str = None):

    # print(content)
    soup = BeautifulSoup(content, 'html5lib')
    print(soup)

    return [elem.text.strip() for elem in sv.select(css_selector_logic,soup)]
        

URL = "https://www.bbc.com/"
SEL_LOGIC = 'a:is(.media__link)'

parse_content(content=get_page_content(url = URL), css_selector_logic=SEL_LOGIC)
